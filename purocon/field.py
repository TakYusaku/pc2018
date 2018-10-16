from flask import *
import requests
import numpy as np

terns = 0
now_terns = 0
fieldSize = []
PointField = np.empty((12, 12))
PositionField = np.empty((12, 12))
friendsPosition_1 = []
friendsPosition_2 = []
enemiesPosition_1 = []
enemiesPosition_2 = []
pos = [friendsPosition_1, friendsPosition_2, enemiesPosition_1, enemiesPosition_2]

def getDirection(data):
    if data[1] == "0":
        return [-1,1]
    elif data[1] == "1":
        return [0,1]
    elif data[1] == "2":
        return [1,1]
    elif data[1] == "3":
        return [-1,0]
    elif data[1] == "4":
        return [0,0]
    elif data[1] == "5":
        return [1,0]
    elif data[1] == "6":
        return [-1,-1]
    elif data[1] == "7":
        return [0,-1]
    elif data[1] == "8":
        return [1,-1]

app = Flask(__name__)

@app.route("/init",methods=["POST"])
def initial(): # curl -X POST localhost:6000/init -H "Content-Type: application/json" -d 'json'
    global fieldSize,PointField,PositionField,pos
    if request.method == "POST":
        data = request.data
        fieldSize = data["fieldSize"]
        p = np.array(data["PointField"])
        PointField = np.reshape(p,(fieldSize[0],fieldSize[1]))
        PositionField = np.zeros((fieldSize[0],fieldSize[1]))
        pos[0] = data["initPosition"][0]
        pos[1] = data["initPosition"][1]
        PositionField[friendsPosition_1[0]-1][friendsPosition_1[1]-1] = 1
        PositionField[friendsPosition_2[0]-1][friendsPosition_2[1]-1] = 1
        now_terns = 1
        return True
    else:
        return False

@app.route("/init/enemy",methods=["POST"])
def initEnemy(): # curl -X POST localhost:6000/init/enemy -H "Content-Type: application/json" -d 'json'
    global PositionField,terns,pos
    if request.method == "POST":
        terns = data["terns"]
        pos[2] = data["init_e_Position"][0]
        pos[3] = data["init_e_Position"][1]
        PositionField[enemiesPosition_1[0]-1][enemiesPosition_1[1]-1] = 2
        PositionField[enemiesPosition_2[0]-1][enemiesPosition_2[1]-1] = 2
        return True
    else:
        return False

@app.route("/judgeaction",methods=["POST"])
def judgeAction(): # curl -X POST localhost:6000/judgeaction -H "Content-Type: application/json" -d 'json'
    global pos,PositionField
    if request.method == "POST":
        data = request.data
        agent = data["agent_num"]
        a = pos[agent-1]
        b = getDirection(data["steps"])
        try:
            r = PositionField[a[0]+b[0],a[1]+b[1]]
            if ((agent == 1 or agent == 2) and r != 6) or ((agent == 3 or agent == 4) and r !=5):
                result = {
                    "bool":True,
                    "message":"move"
                }
            else:
                result = {
                    "bool":False,
                    "message":"RP" # please remove panel
                }
            """
            elif data["steps"][0] == "remove":
                if ((agent == 1 or agent == 2) and r == 6) or ((agent == 3 or agent == 4) and r == 5):
                    result = {
                        "bool":True,
                        "message":"R"
                    }
                else:
                    result = {
                        "bool":False,
                        "message":"NP" # no panel
                    }
            """
        except:
            result = {
                "bool":False,
                "message":"OOF" # out of field
            }
        return json.dumps(result)
"""
data = {
    "agent_num":agent_num,
    "steps":dir_num
}
"""
@app.route("/judgeaction/action",methods=["POST"])
def Action(): # curl -X POST localhost:6000/judgeaction/action -H "Content-Type: application/json" -d 'json'
    global pos,PositionField,now_terns
    if request.method == "POST":
        data = request.data
        agent = data["agent_num"]
        a = pos[agent-1]
        b = getDirection(data["steps"])

        if data["steps"][0] == "move":
            pos[agent-1] = [a[0]+b[0],a[1]+b[1]]
            PositionField[a[0]+b[0],a[1]+b[1]] = num
        elif data["steps"][0] == "remove":
            PositionField[a[0]+b[0],a[1]+b[1]] = 0

        now_terns += 1
        return True
    else:
        return False

"""
        data = {
            "bool":True,
            "agent_num":num,
            "steps":[action,direction]
        }
"""
@app.route("/judgeaction/collision",methods=["POST"])
def collision(): # curl -X POST localhost:6000/judgeaction/collision
    global now_terns
    now_terns += 1
    return True

@app.route("/getposition",methods=["POST"])
def getPosition(): # curl -X POST localhost:6000/getposition
    global pos
    if request.method == "POST":
        data = {
            "bool":True,
            "friendsPosition_1":pos[0],
            "friendsPosition_2":pos[1],
            "enemiesPosition_1":pos[2],
            "enemiesPosition_2":pos[3]
        }
    else:
        data = {
            "bool":False
        }
    data = json.dumps(data)
    return data


@app.route("/show",methods=["POST"])
def show(): # curl -X POST localhost:6000/show
    global now_terns,PositionField,PointField
    if request.method == "POST":
        data = {
            "bool":True,
            "now_terns":now_terns,
            "PositionField":PositionField,
            "PointField":PointField
        }
    else:
        data = {
            "bool":False
        }
    data = json.dumps(data)
    return data


if __name__ == "__main__":
    print('on hello')
    app.run(host="127.0.0.1", port=6000)
