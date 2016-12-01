import psycopg2 as pg
import sys
import itertools
from psycopg2.extras import Json
# import simplejson as json
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






def get_repo_objs(repoList):
    return map(lambda repo:g.get_repo(repo), repoList)



def collect_prs(repoList):
    repos = get_repo_objs(repoList)

    try:
        for repo in itertools.islice(repos, 2, 3):
            print(repo.name)
            prs = repo.get_pulls(state="closed")
            for pr in itertools.islice(prs, 2758, None):
                enhanced_pr = build_obj(pr, repo)
                insert_to_db(conn, enhanced_pr)
    except:
        print(repo.name, pr.number)
        raise





def build_obj(pr, repo):
    pr_service = pullrequest_service(pr, repo)
    success = pr_service.checkSuccess()
    event_count = pr_service.get_event_count()
    user_contrib_count = pr_service.get_user_contrib_count()
    label_count = pr_service.get_label_count()

    obj = pr.raw_data
    obj['success'] = success
    obj['label_count'] = label_count
    obj['event_count'] = event_count
    obj['user_contrib_count'] = user_contrib_count

    return obj


def insert_to_db(connection, pr):
    cur = connection.cursor()
    cur.execute("INSERT INTO paper_pulls (data) VALUES (%s)", [Json(pr)] )
    conn.commit()
    print("successfully added pull request %s" % pr['number'])
    

collect_prs(top_js_repos)
