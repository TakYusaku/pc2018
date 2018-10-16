import numpy as np
import csv
import requests

class Play:
    def __init__(self,terns,qtable_type):
        self.terns = terns
        pos = self.getPosition()
        self.friends_pos = pos[0]
        self.enemies_pos = pos[1]
        self.q_table = self.readQtable(qtable_type)

    def readQtable(self,type):
        fn = 'q_table_' + type + '.csv'
        with open(fn, 'r') as file:
            lst = list(csv.reader(file))
        a = []
        for i in range(144):
            a.append(list(map(float,lst[i])))
        q_table = np.array(a)

        return q_table

    def getPosition(self):
        headers = {"content-type": "application/json"}
        response = requests.post('http://localhost:6000/getposition',headers=headers).json()
        friends_pos = [response["friendsPosition_1"],response["friendsPosition_2"]]
        enemies_pos = [response["enemiesPosition_1"],response["enemiesPosition_2"]]
        return [friends_pos,enemies_pos]

    def getAction(self):
        a = []
        b = False
        observation = self.getStatus(self.friends_pos)
        for i in range(2):
            x = np.argsort(self.q_table[observation[i]])[::-1]
            b = False
            c = 0
            while b!=True:
                headers = {"content-type": "application/json"}
                data = {
                    "agent_num":i+1,
                    "steps":x[c]
                }
                response = requests.post('http://localhost:6000/judgeaction',headers=headers,data=data).json()
                if response["bool"] == True:
                    b = True
                    ms = "move"
                    a.append([ms, x[c]])
                elif response["bool"] == False and response["message"] == "RP":
                    b = True
                    ms = "remove"
                    a.append([ms, x[c]])
                c += 1
        return a

    def doAction(self,action):
        for i in range(2):
            headers = {"content-type": "application/json"}
            data = {
                "agent_num":i+1,
                "steps":action[i]
            }
            response = requests.post('http://localhost:6000/judgeaction/action',headers=headers,data=data).json()

    def getStatus(self, observation):
        obs1 = observation[0]
        obs2 = observation[1]

        a =  np.array([obs1[1]*12 + obs1[0], obs2[1]*12 + obs2[0]])
        return a
