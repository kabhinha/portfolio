from flask import Flask, render_template
from flask import request as res
from pathlib import Path
from Myapps import pchk, hn, etrack
import requests, os

BASE_DIR = Path(__file__).parent
os.chdir(BASE_DIR)
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home/index.html")

@app.route("/dev/<string:page_name>")
def comp(page_name):
    return render_template(page_name)

@app.route("/projects/py/passwd-checker", methods=['POST', 'GET'])
def passwdcheckr():
    if res.method == "POST":
        name = res.form["name"]
        passwd = res.form["passwd"]
        hashes, tail = pchk.request_data(passwd, requests.get)
        count = pchk.count_leaks(hashes, tail)
        vars = {"password":passwd, "re":True}
        if count:
            vars["result"], vars["status"] = f"Hey, {name} This password has been seen {count} times before This password has previously appeared in a data breach and should never be used. If you've ever used it anywhere before, change it!", "danger"
        else:
            vars["result"], vars["status"] = f"Hey, {name} this is good to go no leak found..!!", "success"
        return render_template("project/passwd-chekker.html", **vars)
    return render_template("project/passwd-chekker.html", re=False)

@app.route("/projects/py/hacker-news", methods=['POST', 'GET'])
def heckernews():
    titles, links, votes, today = hn.publish()
    return render_template("project/hackers-news.html", titles=enumerate(titles), links=links, votes=votes, today=today)

@app.route("/projects/py/expense-tracker", methods=['POST', 'GET'])
def eetracker():
    if res.method == "POST":
        passwd = res.form["passwd"]
        print(passwd)
    return render_template("project/expense-tracker.html")

@app.route("/projects/py/expense-tracker/disp", methods=['POST', 'GET'])
def eetracker_show():
    if res.method == "POST":
        passwd = res.form["passwd"]
        print(passwd)
    return render_template("project/expense-tracker_disp.html")
