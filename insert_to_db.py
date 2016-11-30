import psycopg2 as pg
import simplejson as json
import configparser

from github import Github

from pullrequest_service import pullrequest_service


config = configparser.ConfigParser()
config.read('study.cfg')


try:
    connstring = "dbname=%s user=%s" % (config.get("postgresql", "dbname"), config.get("postgresql", "dbuser"))
    conn = pg.connect(connstring)
except:
    print("I am unable to connect to the database")


g = Github(config.get("github", "username"), config.get("github", "password"))
top_js_repos = [
    "d3/d3",
    "facebook/react",
    "angular/angular.js",
    "jquery/jquery",
    "facebook/react-native",
    "meteor/meteor",
    "vuejs/vue",
    "hakimel/reveal.js",
    "impress/impress.js",
    "nodejs/node",
    "mrdoob/three.js",
    "socketio/socket.io",
    "moment/moment",
    "expressjs/express"
    "chartjs/Chart.js",
    "reactjs/redux",
    "jashkenas/backbone",
    "gulpjs/gulp",
    "babel/babel",
    "ReactTraining/react-router",
    "emberjs/ember.js"
]





def setup_db(connection):
    cur = connection.cursor()
    cur.execute("CREATE TABLE paper_pulls (id serial, data json);")
    conn.commit()

def get_repo_objs(repoList):
    return map(lambda repo:g.get_repo(repo), repoList)


def collect_prs(repoList):
    repos = get_repo_objs(repoList)
    prlist = []
    for repo in repos:
        prs = repo.get_pulls(state="closed")
        enhanced_prs = enhance_prs(prs, repo)
        for pr in enhanced_prs:
            prlist.append(pr)

    return prlist


def enhance_prs(prs, repo):
    enhanced_prs = []
    for pr in prs:
        enhanced_prs.append(build_obj(pr, repo))

    return enhanced_prs



def build_obj(pr, repo):
    pr_service = pullrequest_service(pr, repo)
    obj = {
        # labelCount: pr_service.getLabelCount(),
        # 'commentCount': pr_service.get_comment_count(),
        # commitCount: pr_service.getCommitCount(),
        # starsCount: pr_service.getStarsCount(),
        # size: pr_service.getSize(),
        # changedFiles: pr_service.getchangedFiles()
        'rawData': pr_service.get_raw_data(),


        'success': pr_service.checkSuccess()
    }
    return obj


def insert_to_db(connection, prs):
    cur = connection.cursor()
    for pr in prs:
        print(pr)
        cur.execute("INSERT INTO paper_pulls (data) VALUES (%s)" % json.dumps(pr))
        conn.commit()
    



# setup_db(conn)
prs = collect_prs(top_js_repos)
insert_to_db(conn, prs)
