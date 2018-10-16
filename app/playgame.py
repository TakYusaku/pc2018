import numpy as np
import csv

class Play:
    def __init__(self,terns,qtable_type):
        self.terns = terns
        self.friends_pos = [[,],[,]]
        self.enemies_pos = [[,],[,]]
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
        friends_pos = [[,],[,]]
        enemies_pos = [[,],[,]]
        return [friends_pos,enemies_pos]

    def getAction(self,q_table,observation):
        a = []
        b = False
        for i in range(2):
            x = np.argsort(q_table[observation[i]])[::-1]
            b = False
            c = 0
            while b!=True:
                b, d, ms, next_pos = env.judAc(i+1+n, x[c])  ########## check #############
                c += 1
            a.append([d, ms, next_pos])
        return a
