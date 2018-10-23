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
    global field_info,game
    field_info = qr.Decode()
    info = {
        "fieldSize":field_info[0],
        "initPosition":field_info[1],
        "PointField":field_info[2]
    }
    headers = {
        'Content-Type': 'application/json',
    }
    game.reset(terns,"QL")
    #data = json.dumps(info)
    try:
        response = requests.post('http://localhost:8000/init', data=info) # headers=headers,
    except:
        return ender_template('error.html')

    return ender_template('post_fieldinfo.html')


@app.route("/added_info",methods=["POST"]) # ok
def fieldInfo():
    global terns
    if request.method == "POST":
        getInfo = request.form.getlist("info")
        terns = int(getInfo)
        return render_template('playgame.html')


@app.route("/play/e_action",methods=["GET","POST"])
def eAction():
    global game
    if request.method == "POST": # data = {"action":"move or remove", "direction":"lu"}
        data = request.data
        r = game.doAction(data,2,)
        return True

@app.route("/play/get_action",methods=["GET","POST"])
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
            r = game.doAction(dt["actions"],0)
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
