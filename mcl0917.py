# learning agent by Monte Carlo method

import gym
import requests
import numpy as np
import csv
import matplotlib.pyplot as pl
from collections import deque
import time
import threading
#import # 敵のデータ

def getAction(env, q_table, observation, episode,choice): # get action (array)  # フィールド外は再計算
    #epsilon = 0.5 * (1 / (episode + 1))
    epsilon = 0.5
    a = []
    b = False
    n = 2
    if choice == 0:
        n = 2
    elif choice == 1:
        n = 0

    for i in range(2):
        if np.random.uniform(0, 1) > epsilon:  # e-greedy low is off
            x = np.argsort(q_table[observation[i]])[::-1]
            b = False
            c = 0
            while b!=True:
                b, d, ms, next_pos = env.judAc(i+1+n, x[c])
                c += 1
            a.append([d, ms, next_pos])

        else: # e-greedy low is on
            b = False
            while b!=True:
                pa = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
                b, d, ms, next_pos = env.judAc(i+1+n, pa)
            a.append([d, ms, next_pos])

    return a  # [[int(direction), str(movement), list(next position)],[]]
"""
def getAction(env, q_table, observation, episode,choice): # get action (array)  # フィールド外は罰金
    #epsilon = 0.5 * (1 / (episode + 1))
    epsilon = 0.5
    a = []
    b = False
    n = 2
    if choice == 0:
        n = 2
    elif choice == 1:
        n = 0

    for i in range(2):
        if np.random.uniform(0, 1) > epsilon:  # e-greedy low is off
            x = np.argsort(q_table[observation[i]])[::-1]
            b, d, ms, next_pos = env.judAc(i+1+n, x[0])
            a.append([d, ms, next_pos])

        else: # e-greedy low is on
            pa = np.random.choice([0, 1, 2, 3, 4, 5, 6, 7, 8])
            b, d, ms, next_pos = env.judAc(i+1+n, pa)
            a.append([d, ms, next_pos])
    return a  # [[int(direction), str(movement), list(next position)],[]]
"""

# [] update Qtables
def updateQtable(q_table, memory):#observation, action, reward, next_observation):
    gamma = 0.99 # time discount rate
    alpha = 0.1 # learning rate
    total_reward_t = 0
    while (memory.len() > 0):
        (state, action, reward) = memory.sample()
        total_reward_t = gamma * total_reward_t       # 時間割引率をかける
        # Q関数を更新
        q_table[state, action[0]] = q_table[state, action[0]] + alpha*(reward+total_reward_t-q_table[state, action[0]])
        total_reward_t = total_reward_t + reward    # ステップtより先でもらえた報酬の合計を更新

    return q_table


class Memory:
    def __init__(self, max_size):
        self.buffer = deque(maxlen=max_size)

    def add(self, experience):
        self.buffer.append(experience)

    def sample(self):
        return self.buffer.pop()

    def len(self):
        return len(self.buffer)

"""
# [] main processing
if __name__ == '__main__':
    # [] make environment
    env = gym.make('procon18env-v0')
    #ene = .make('') # make enemy
    num_episode = 50 # 1050

    is_learned = 0 #学習終了フラグ
    is_render = 0 #描画フラグ

    win1 = 0
    win2 = 0

    # [] make Qtable (state,action)
    #q_table = np.zeros((144, 9))

    # read q tables from csv file
    with open('q_table_MCM.csv', 'r') as file:
        lst = list(csv.reader(file))
    a = []
    for i in range(144):
        a.append(list(map(float,lst[i])))
    q_table = np.array(a)

    for episode in range(num_episode):
        observation = env.reset(episode+1) #array
        terns = env.num_terns
        row = env.Row
        column = env.Column
        total_reward = 0
        memory1 = Memory(terns)
        memory2 = Memory(terns)

        for i in range(terns):
            env.steps = i+1
            # choose action (num)
            ob = env.getStatus(observation)
            action = getAction(env, q_table, observation, episode) # array


            enemy_action = ene.get_enemy_Action() # array [int, int]
            for i in range(2):
                if action[i][3] == enemy_action[i][1]: # 移動先が被ったら停留
                    action[i][0] == 4
                    enemy_action[i][0] == 4


            # step
            next_observation, reward, done, _ = env.step(action, "M")
            #ene.step(enemy_action)

            memory1.add((ob[0], action[0], reward))
            memory2.add((ob[1], action[1], reward))

            total_reward += reward
            observation = next_observation

            if done:
                # update q_table
                q_table = updateQtable(q_table, memory1)
                q_table = updateQtable(q_table, memory2)
                break
        a = np.array([episode + 1, total_reward])
        print(env.judVoL())
        if env.judVoL() == "Win_1":
            win1 += 1
        else:
            win2 += 1
        print(episode)

    # save q table
    with open('q_table_MCM.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(q_table)

    print(win1)
    print(win2)
"""
