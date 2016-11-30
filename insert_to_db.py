import psycopg2 as pg
import simplejson as json
import ConfigParser

from github import Github

from pullrequest_service import pullrequest_service


config = ConfigParser.ConfigParser()
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
    prs = []
    for repo in repos:
        prs = repo.get_pulls(state="closed")
        enhanced_prs(prs, repo)


def enhance_pr(prs, repo):
    for pr in prs:
        pr = build_obj(pr, repo, g)



def build_obj(pr, repo, github):
    pr_service = pullrequest_service(pr, repo, github)
    obj = {
        # labelCount: pr_service.getLabelCount(),
        commentCount: pr_service.get_comment_count(),
        # commitCount: pr_service.getCommitCount(),
        # starsCount: pr_service.getStarsCount(),
        # size: pr_service.getSize(),
        # changedFiles: pr_service.getchangedFiles()
        rawData: pr_service.get_raw_data()


        'success': pr_service.checkSuccess()
    }
    return obj

class pullrequest_service():
    def __init__(self, pr, repo):
        self.pr = pr
        self.repo = repo

    def getLabelCount(self):
        return self.pr.labels.length

    def getchangedFiles(self):
        return self.pr.changed_files

    def checkSuccess(self):
        events = self.repo.get_issue(self.pr.number).get_events()
        close_event = next((obj for obj in events if obj.event == "closed"), None)

        return self.pr.merged or close_event.commit_id if hasattr(close_event, 'commit_id') else None

    def get_raw_data(self):
        return self.pr.raw_data


setup_db(conn)
collect_prs(top_js_repos)
