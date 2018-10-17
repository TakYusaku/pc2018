#environment
#last update 2018-09-04 14:14

import requests
import sys
import gym
import numpy as np
import json
import random
import gym.spaces


class procon18Env(gym.Env): #define environment
    # initial con
    metadata = {'render.modes': ['human', 'ansi']} #omajinai
    num_terns = 0 #number of terns
    Row = 0 #row of field
    Column = 0 #column of field
    pf = [] #field of point

    def __init__(self): #initialization
        super().__init__()
        #make field
        #fs = self.makeField()
        #initialization of agent1
        self._1action_space = gym.spaces.Discrete(9) #行動(Action)の張る空間
        self._1reward_range = [-120.,100.] #報酬の最小値と最大値のリスト

        #initialization of agent2
        self._2action_space = gym.spaces.Discrete(9) #行動(Action)の張る空間
        self._2reward_range = [-120.,100.] #報酬の最小値と最大値のリスト

        #initialization of agent3
        self._3action_space = gym.spaces.Discrete(9) #行動(Action)の張る空間
        self._3reward_range = [-120.,100.] #報酬の最小値と最大値のリスト

        #initialization of agent4
        self._4action_space = gym.spaces.Discrete(9) #行動(Action)の張る空間
        self._4reward_range = [-120.,100.] #報酬の最小値と最大値のリスト

        #self.reset()


    def makeField(self):  # make point field . return is tuple of (Row, Column)   // verified
        response = requests.get('http://localhost:8000/start') #gets data
        f = response.text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
        iv_list = [int(i) for i in f.split()] #listing initial value
        self.num_terns = iv_list[0] #number of terns
        self.Row = iv_list[1] #row of field
        self.Column = iv_list[2] #column of field
        fs = (self.Row, self.Column) # tuple
        self.pf = [] #field of point
        for i in range(self.Row * self.Column):
            self.pf.append(iv_list[i + 3])
        """
        for i in range(Row):
            for j in range(Column):
                if i != 0 and j == 0:
                    self.pf.append('\n'+str(iv_list[i*self.Column + j + 3]))
                else:
                    self.pf.append(str(iv_list[i*self.Column + j + 3]))
        """

        return fs

    def reset(self, pattern): # initialization of position,points and steps  (rv is array of position)
        fs = self.makeField()
        self._1observation_space = gym.spaces.Box( #観測値(Observation)の張る空間,環境から得られる値
            low = -16, #x軸の最値,y軸の最小値,pointsの最小値
            high = 16, #x,y,pointsの最大値
            shape = fs #yousosu
        )
        self._2observation_space = gym.spaces.Box( #観測値(Observation)の張る空間,環境から得られる値
            low = -16, #x軸の最値,y軸の最小値,pointsの最小値
            high = 16, #x,y,pointsの最大値
            shape = fs #yousosu
        )
        self._3observation_space = gym.spaces.Box( #観測値(Observation)の張る空間,環境から得られる値
            low = -16, #x軸の最値,y軸の最小値,pointsの最小値
            high = 16, #x,y,pointsの最大値
            shape = fs #yousosu
        )
        self._4observation_space = gym.spaces.Box( #観測値(Observation)の張る空間,環境から得られる値
            low = -16, #x軸の最値,y軸の最小値,pointsの最小値
            high = 16, #x,y,pointsの最大値
            shape = fs #yousosu
        )
        observation = []
        if pattern == 0:
            self._1pos = self.getPosition(1)
            self._2pos = self.getPosition(2)
            self._3pos = self.getPosition(3)
            self._4pos = self.getPosition(4)
        elif pattern == 1:
            self._1pos = self.getPosition(3)
            self._2pos = self.getPosition(4)
            self._3pos = self.getPosition(1)
            self._4pos = self.getPosition(2)

        observation.append([self._1pos, self._2pos])
        observation.append([self._3pos, self._4pos])
        self.points = 0
        self.steps = 0
        self.pattern = pattern
        return observation

    def step(self, action_f, action_e,terns): # processing of 1step (rv is observation,reward,done,info)
        if self.pattern == 0:
            if action_e[0][1] == "move":
                self.Move(3, action_e[0][0])
            elif action_e[0][1] == "remove":
                self.Remove(3, action_e[0][0])
            if action_e[1][1] == "move":
                self.Move(4, action_e[1][0])
            elif action_e[1][1] == "remove":
                self.Remove(4, action_e[1][0])
            #observation_e = self._observe(2)

            if action_f[0][1] == "move":
                self.Move(1, action_f[0][0])
            elif action_f[0][1] == "remove":
                self.Remove(1, action_f[0][0])
            if action_f[1][1] == "move":
                self.Move(2, action_f[1][0])
            elif action_f[1][1] == "remove":
                self.Remove(2, action_f[1][0])
            #observation_f = self._observe(1)#array

        elif self.pattern == 1:
            if action_e[0][1] == "move":
                self.Move(1, action_e[0][0])
            elif action_e[0][1] == "remove":
                self.Remove(1, action_e[0][0])
            if action_e[1][1] == "move":
                self.Move(2, action_e[1][0])
            elif action_e[1][1] == "remove":
                self.Remove(2, action_e[1][0])
            #observation_e = self._observe(2)

            if action_f[0][1] == "move":
                self.Move(3, action_f[0][0])
            elif action_f[0][1] == "remove":
                self.Remove(3, action_f[0][0])
            if action_f[1][1] == "move":
                self.Move(4, action_f[1][0])
            elif action_f[1][1] == "remove":
                self.Remove(4, action_f[1][0])
            #observation_f = self._observe(1)#array

        observation = self._observe()
        reward_Q = self._get_reward_QL() #str
        reward_M = self._get_reward_MCM(terns)
        reward = np.array([float(int(reward_Q)),float(int(reward_M))])
        self.done = self._is_done() #num
        return observation, reward, self.done, {}

    def _close(self):
        pass

    def _seed(self, seed=None):
        pass

    def _get_reward_QL(self): # return reward (str)  by q-learning
        if self.steps == self.num_terns: # if final
            if self.judVoL() == "Win_1": #if won
                return "10"
            else:
                return "-5"
        else:
            p = self.calcPoint()
            if p[2] >= p[5]:  # 試合途中，同点か勝っているとき
                return "2"
            else:
                return "-1"

    def _get_reward_MCM(self,terns):
        if self._is_done():
            if self.judVoL() == "Win_2":
                return "10"
            else:
                p = self.calcPoint()
                if p[5] > 0: # 負けて合計ポイントが正なら
                    r = terns * 0.85 * (-1)
                    return str(int(r))
                else:
                    return str(int(terns * 0.95 * (-1)))
        else:
            return "1"

    def _observe(self): #position of agent (array)  // verified
        observation = []
        if self.pattern == 0:
            observation.append([self.getPosition(1), self.getPosition(2)])
            observation.append([self.getPosition(3), self.getPosition(4)])

        elif self.pattern == 1:
            observation.append([self.getPosition(3), self.getPosition(4)])
            observation.append([self.getPosition(1), self.getPosition(2)])
        return observation

    def _is_done(self): #done or not (bool)
        if self.steps == self.num_terns or self.steps > self.num_terns:
            return True
        else:
            return False

    # show で作る list of log  (rv is list)  // verified
    def show(self):
        f = requests.post('http://localhost:8000/show').text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
        iv_list = [int(i) for i in f.split()]
        lf = []
        for i in range(self.Row):
            l = []
            for j in range(self.Column):
                l.append(iv_list[self.Row * self.Column + self.Column * i + j])
            lf.append(l)
        return lf

    def serPosition(self, lf, usr1, usr2, tile_num): #list  // verified
        tiles = []
        for i in range(self.Row):
            for j in range(self.Column):
                if lf[i][j] == usr1 or lf[i][j] == usr2 or lf[i][j] == tile_num:
                    tiles.append({"y": i,"x": j})
                else:
                    pass
        return tiles

    def gJdata(self): #得点計算のJSON json  // verified
        lf = self.show()
        if self.pattern == 0:
            data = {
                "field":{
                    "scores": self.pf ,
                    "height": self.Row ,
                    "width" : self.Column
                },
                "teams":[
                    { "tiles" : self.serPosition(lf, 1, 2, 5)},
                    { "tiles" : self.serPosition(lf, 3, 4, 6)}
                ]
            }
        else:
            data = {
                "field":{
                    "scores": self.pf ,
                    "height": self.Row ,
                    "width" : self.Column
                },
                "teams":[
                    { "tiles" : self.serPosition(lf, 3, 4, 6)},
                    { "tiles" : self.serPosition(lf, 1, 2, 5)}
                ]
            }
        return data


    def calcPoint(self): # Calculate Point  array  // verified
        headers = {
         'content-type': 'application/json',
         'x-api-key': 'yMNijQ0b5t5uEkfdgXVgWmypvJaBdcY2Kd3E9XF3',
        }

        data = json.dumps(self.gJdata())
        response = requests.post('https://42isf6z498.execute-api.ap-northeast-1.amazonaws.com/dev', headers=headers, data=data).json()
        print(response)
        self.friend_tilePoint = response['data'][0]['tile_point']
        self.friend_territoryPoint = response['data'][0]['territory_point']
        self.friend_totalPoint = self.friend_tilePoint + self.friend_territoryPoint

        self.enemy_tilePoint = response['data'][1]['tile_point']
        self.enemy_territoryPoint = response['data'][1]['territory_point']
        self.enemy_totalPoint = self.enemy_tilePoint + self.enemy_territoryPoint
        p = [self.friend_tilePoint, self.friend_territoryPoint, self.friend_totalPoint, self.enemy_tilePoint, self.enemy_territoryPoint, self.enemy_totalPoint]
        return p

    def judVoL(self): #judge won or lose  str  // verified
        p = self.calcPoint()
        if p[2] > p[5]: # won friends
            return "Win_1"
        elif p[2] == p[5]: # draw
            if p[0] > p[3]: # won friends (tile point)
                return "Win_1"
            elif p[0] == p[3]:
                re = random.choice(["Win_1", "Win_2"])
                return re
        else:
            return "Win_2"


    def getPosition(self, usr): #get position (array)  // verified
        data = [
          ('usr', usr),
        ]

        response = requests.post('http://localhost:8000/usrpoint', data=data)
        f = response.text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
        pos_array =[int(i) for i in f.split()]
        return pos_array  # [x(column), y(row)]


    def judAc(self, usr, dir):   # judge Actionb   // verified
        data = [
          ('usr', usr),
          ('d', self.gaStr(dir)),
        ]
        f = requests.post('http://localhost:8000/judgedirection', data = data).text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
        iv_list = [i for i in f.split()]
        i = [int(iv_list[0]),int(iv_list[1])]

        if iv_list[2] == "Error":
            return False, dir, "oof", i
        elif iv_list[2] == "is_panel":
            return True, dir, "remove", i
        else:
            return True, dir, "move", i


    def Move(self, usr, dir): #move agent  // verified
        data = [
          ('usr', usr),
          ('d', self.gaStr(dir)),
        ]
        response = requests.post('http://localhost:8000/move', data=data)


    def Remove(self, usr, dir): #remove panels  // verified
        data = [
         ('usr', usr),
         ('d', self.gaStr(dir)),
        ]
        response = requests.post('http://localhost:8000/remove', data=data)


    # dim2 -> dim1  フィールドのマス目に番号を振る #array  // verified
    def getStatus(self, observation): #
        obs1 = observation[0]
        obs2 = observation[1]

        a =  np.array([obs1[1]*12 + obs1[0], obs2[1]*12 + obs2[0]])
        return a  # [int, int]


    def gaStr(self, action): # get action str // verified
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

    def grDir(self, action):  # // get reverse action (str)
        if action == 0:
            return "rd"
        elif action == 1:
            return "d"
        elif action == 2:
            return "ld"
        elif action == 3:
            return "r"
        elif action == 4:
            return "s"
        elif action == 5:
            return "l"
        elif action == 6:
            return "ru"
        elif action == 7:
            return "u"
        elif action == 8:
            return "lu"
