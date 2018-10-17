#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import time
from flask import *
import sys,os
sys.path.append('../qr')
import test_qr as qr
import playgame as pg
import requests
import json

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

app = Flask(__name__)
terns = 0
game = pg.Play()
field_info = []
enemy_1 = []
enemy_2 = []


@app.route("/")
def hello():
    html = render_template('top.html')
    return html

@app.route("/read_qr")
def readQR():
    global field_info
    field_info = qr.Decode()
    info = {
        "fieldSize":field_info[0],
        "initPosition":field_info[1],
        "PointField":field_info[2]
    }
    headers = {
        'Content-Type': 'application/json',
    }
    data = json.dumps(info)
    try:
        response = requests.post('http://localhost:6000/init', headers=headers, data=data)
        if response:
            pass
        else:
            return """<script type="text/javascript">
            　           alert("False")
                      </script>"""
    except:
        return """<script type="text/javascript">
        　           alert("error")
                  </script>"""
    return render_template('post_fieldinfo.html')


@app.route("/field_info",methods=["POST"])
def fieldInfo():
    global terns,enemy_1,enemy_2
    if request.method == "POST":
        getInfo = request.form.getlist("info")
        terns = int(getInfo[0])
        enemy_1 = [int(getInfo[1]),int(getInfo[2])]
        enemy_2 = [int(getInfo[3]),int(getInfo[4])]
        info = {
            "terns":terns,
            "init_e_Position":[enemy_1,enemy_2]
        }
        headers = {
            'Content-Type': 'application/json',
        }
        data = json.dumps(info)
        try:
            response = requests.post('http://localhost:6000/init/enemy', headers=headers, data=data)
            if response:
                pass
            else:
                return """<script type="text/javascript">
                　           alert("False")
                          </script>"""
        except:
            return """<script type="text/javascript">
            　           alert("error")
                      </script>"""
        return render_template('playgame.html')


@app.route("/play_start")
def playGame():
    global game,terns
    game.reset(terns,"QL")
    html = render_template('start.html')
    return html

@app.route("/play/action",methods=["GET","POST"])
def playGame():
    global game
    if request.method == "GET":
        a = game.getAction()
        return a
    elif request.method == "POST":
        data = request.data
        if dt["collision_or_not"]:
            response = requests.post('http://localhost:6000/judgeaction/collision')
        else:
            r = game.doAction(dt["actions"])
        return True
"""
data = {
    "collision_or_not": True or False,
    "actions":[[action,direction],[f2]]
}
"""

if __name__ == "__main__":
    print('on hello')
    app.run(host="127.0.0.1", port=5000)
