from flask import Flask
from flask import jsonify

import psycopg2 as pg


import simplejson as json
# from flask import json



# from typing import List

# app = Flask(__name__)


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


# @app.route("/")
# def huhu():
#     # return 'hallo'
#     pullCount = get_merged_pr_count(g.get_repo('d3/d3'))
#     return jsonify(huhu=pullCount)


def compare_prs(repoList):
    pass
    # for repo in repoList
    #     g.get_repo(repo)


def get_merged_pr_count(repo):
    pulls = repo.get_pulls()
    pulls_count = 0
    success_count = 0
    # Fix no count available on pulls list
    for _ in pulls:
        pr = build_obj(_, repo, g)
        if pr['success']:
            success_count += 1
        else:
            pulls_count += 1

    return (pulls_count, success_count)


# print(get_merged_pr_count(g.get_repo('angular/angular.js')))

# def get_repos(repoList: List[str]):
#     repos = []
#     for repo_name in repoList:
#         repos.append(g.get_repo(repo_name))
#     return repos
#
#
#
# def get_issues_of_repos(repos):
#     issues = []
#     for repo in repos:
#         for issue in repo.get_issues():
#             issues.append(issue)
#     return issues

# example_issue = repo.get_issues()
# example_issue2 = repo.get_issue(4)
#
# events = example_issue2.get_events()
#
# repos = get_repos(repos_names)
# issues = get_issues_of_repos(repos)
