import psycopg2 as pg
import sys
import itertools
from psycopg2.extras import Json
# import simplejson as json
import configparser

from github import Github
from github import GithubException

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



def update_sql():
    update_label_count(g.get_repo("d3/d3"), "d3")
    update_label_count(g.get_repo("facebook/react"), "react")
    

def update_label_count(repo, reponame):
    try:
        key_name = "label_count"
        cur = conn.cursor()
        cursel = conn.cursor('select')
        cursel.execute("select * from paper_pulls where data->%s IS NULL AND data->'base'->'repo'->>'name' = %s", (key_name, reponame))
        for e in cursel:
            issue_number = e[1]['number']
            value = get_event_count(repo, issue_number)
            sql_update_execution( key_name, value, e[0])
        conn.commit()
    except:
        conn.commit()
        raise


def get_event_count(repo, issue_number):
    events = repo.get_issue(issue_number).get_events()
    counter = 0
    for event in events:
        counter+=1
        return counter



def sql_update_execution( key_name, value, id):
    print ( cur.execute("update paper_pulls set data = to_json(jsonb_set(to_jsonb(data), '{\"%s\"}', to_jsonb(%s))) where id=%s;", (key_name, label_count, id)) )
    print("success of %s" % id)


update_sql()
