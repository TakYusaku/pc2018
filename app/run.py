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


app = Flask(__name__)
terns = 0
game = pg.Play()
field_info = []
enemy_1 = []
enemy_2 = []


@app.route("/")  # ok
def hello():
    html = render_template('top.html')
    return html

@app.route("/read_qr") # ok
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
    #data = json.dumps(info)
    try:
        response = requests.post('http://localhost:8000/init', data=info) # headers=headers,
    except:
        return ender_template('error_qr.html')

    return ender_template('post_fieldinfo.html')


@app.route("/enemy_info",methods=["POST"])
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
        #data = json.dumps(info)
        try:
            response = requests.post('http://localhost:8000/init/enemy_info', data=data) #  headers=headers,
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
            response = requests.post('')
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
