#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from flask import Flask, render_template,*,request
import sys,os
sys.path.append('../qr')
import test_qr as qr
import playgame
import requests
import json

app = Flask(__name__)
field_info = []
terns = 0
enemy_1 = []
enemy_2 = []


@app.route("/")
def hello():
    html = render_template('start.html')
    return html

@app.route("/read_qr")
def readQR():
    global field_info
    field_info = qr.Decode()
    return render_template('post_fieldinfo.html')

@app.route("/field_info",methods=["GET","POST"])
def fieldInfo():
    global terns,enemy_1,enemy_2
    if request.method == "POST":
        getInfo = request.form.getlist("info")
        terns = int(getInfo[0])
        enemy_1 = [int(getInfo[1]),int(getInfo[2])]
        enemy_2 = [int(getInfo[3]),int(getInfo[4])]
        return render_template('playgame.html')
    elif request.method == "GET":
        global field_info
        info = {
            "gameTerns":terns,
            "fieldSize":field_info[0],
            "pointField":field_info[2]
        }
        return info


@app.route("/play",methods=["POST"])
def playGame():
    if request.method == "POST":
        data = [
          ('usr', usr),
          ('d', gaStr(dir)),
        ]
        f = requests.post('http://localhost:8000/judgedirection', data = data).text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")


def gaStr(action): # get action str // verified
    if action == 0:
        return "lu"
    elif action == 1:
        return "u"
    elif action == 2:
        return "ru"
    elif action == 3:
        return "l"
    elif action == 4:
        return "s"
    elif action == 5:
        return "r"
    elif action == 6:
        return "ld"
    elif action == 7:
        return "d"
    elif action == 8:
        return "rd"

if __name__ == "__main__":
    print('on hello')
    app.run(host="127.0.0.1", port=5000)
