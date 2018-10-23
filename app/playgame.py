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


    def getAction(self,cnt):
        a = []
        c = cnt
        cnt_a = []
        observation = self.getStatus(self.friends_pos)
        for i in range(2):
            x = np.argsort(self.q_table[observation[i]])[::-1]
            b = False
            while b!=True:
                data = [
                  ('usr', i+1),
                  ('d', self.gaStr(x[c[i]])),
                ]
                f = requests.post('http://localhost:8000/judgedirection', data = data).text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
                iv_list = [i for i in f.split()]
                i = [int(iv_list[0]),int(iv_list[1])]
                if iv_list[2] == "Error":
                    c[i] += 1
                elif iv_list[2] == "is_panel":
                    a.append(["remove", self.gaStr(x[c[i]])])
                    b = True
                    cnt_a.append(c[i]+1)
                else:
                    a.append(["move", self.gaStr(x[c[i]])])
                    b = True
                    cnt_a.append(c[i]+1)
        return a,cnt_a


    def doAction(self,data,f_or_e):
        if data["action"] == "remove":
            data = {
                "usr":str(i+1+f_or_e),
                "d":action[i]
            }
            response = requests.post('http://localhost:8000/remove',data=data)
        elif data["action"] == "move":
            data = {
                "usr":str(i+1+f_or_e),
                "d":action[i]
            }
            response = requests.post('http://localhost:8000/move',data=data)
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
