import numpy as np
import csv
import requests

class Play:
    def reset(self,terns,size,qtable_type): # ok
        self.terns = terns
        self.size = size
        self.friends_pos = []
        for i in range(2):
            self.friends_pos.append(elf.getPosition(i+1))
        self.enemies_pos = [[self.size[0]-(self.friends_pos[0][0]+1),self.size[1]-(self.friends_pos[0][1]+1)],[self.size[0]-(self.friends_pos[1][0]+1),self.size[1]-(self.friends_pos[1][1]+1)]]
        self.q_table = self.readQtable(qtable_type)

    def readQtable(self,type): # ok
        fn = '../q_table_' + type + '.csv'
        with open(fn, 'r') as file:
            lst = list(csv.reader(file))
        a = []
        for i in range(144):
            a.append(list(map(float,lst[i])))
        q_table = np.array(a)

        return q_table

    def getPosition(self, usr): # ok
        data = [
          ('usr', usr),
        ]
        response = requests.post('http://localhost:8000/usrpoint', data=data)
        f = response.text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
        pos_array =[int(i) for i in f.split()]
        return pos_array

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

    def doAction(self,data,f_or_e):
        if data["action"] == "remove":
            data = {
                "usr":str(i+1+f_or_e),
                "d":action[i]
            }
            response = requests.post('http://localhost:8000/remove',data=data)
        """
        for i in range(2):
            data = {
                "usr":str(i+1+f_or_e),
                "d":action[i]
            }
            response = requests.post('http:/_/localhost:8000/judgeaction/action',data=data)
        """

    def getStatus(self, observation):
        obs1 = observation[0]
        obs2 = observation[1]

        a =  np.array([obs1[1]*12 + obs1[0], obs2[1]*12 + obs2[0]])
        return a

    def gaStr(self,action): # get action str // verified
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
