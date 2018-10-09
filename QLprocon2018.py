# array[row(y)][column(x)]
# https://qiita.com/ishizakiiii/items/75bc2176a1e0b65bdd16
# learning agent by Q-learning

import gym
import requests
import numpy as np
import csv
import matplotlib.pyplot as pl
#import # 敵のデータ

# update Qtables
def updateQtable(env, q_table, observation, action, reward, next_observation):
    gamma = 0.99 # time discount rate
    alpha = 0.5 # learning rate

    #行動後の状態で得られる最大行動価値　(つまり最も良い行動を選ぶ)
    next_position = env.getStatus(next_observation)
    next_max_q_value = np.array([max(q_table[next_position[0]]),max(q_table[next_position[1]])])

    # 行動前の状態の行動価値
    position = env.getStatus(observation)
    q_value = np.array([q_table[position[0],action[0][0]], q_table[position[1],action[1][0]]])

    #  行動価値関数の更新
    q_table[position[0],action[0][0]] = q_value[0] + alpha * (reward + gamma * next_max_q_value[0] - q_value[0])
    q_table[position[1],action[1][0]] = q_value[1] + alpha * (reward + gamma * next_max_q_value[1] - q_value[1])

    return q_table

# get action (list)
def getAction(env, q_table, observation, episode, choice):
    epsilon = 0.5 * (1 / (episode + 1))
    a = []
    b = False
    if choice == 0:
        n = 0
    elif choice == 1:
        n = 2
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

    return a  # [int, str, list]

def readQtable(type):
    fn = 'q_table_' + type + '.csv'
    with open(fn, 'r') as file:
        lst = list(csv.reader(file))
    a = []
    for i in range(144):
        a.append(list(map(float,lst[i])))
    q_table = np.array(a)

    return q_table

def writeQtable(type, q_table):
    fn = 'q_table_' + type + '.csv'
    with open(fn, 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(q_table)


def gA_Enemy(env, q_table, observation):
    position = env.getStatus(observation)
    a = []
    for i in range(2):
        q = q_table[position[i]]
        x = np.argsort(q)[::-1]
        b = False
        c = 0
        while b!=True:
            b, d, ms, next_pos = env.judAc(i+3, x[c])
            c += 1
        a.append([d, ms, next_pos])
    return a

"""
# [] main processing
if __name__ == '__main__':
    # [] make environment
    env = gym.make('procon18env-v0')
    num_episode = 10

    is_learned = 0 #学習終了フラグ
    is_render = 0 #描画フラグ
    win1 = 0
    win2 = 0

    # [] make Qtable (state,action)
    #q_table = np.zeros((144, 9))

    # read q tables from csv file
    q_table = readQtable('QL')
    q_table_Enemy = readQtable('MCM')


    #learning
    for episode in range(num_episode):
        #initialization environments
        observation = env._reset(episode+1) #array
        observation_Enemy = env._observe('E')
        terns = env.num_terns
        row = env.Row
        column = env.Column
        total_reward = 0

        for i in range(terns):
            env.steps = i+1
            # choose action (num)
            action = getAction(env, q_table, observation, episode) # list
            enemy_action = gA_Enemy(env, q_table_Enemy, observation_Enemy)


        for i in range(2):
            if action[i][2] == enemy_action[i][2]: # 移動先が被ったら停留
                action[i][0] == 4
                enemy_action[i][0] == 4


            # step
            next_observation, reward, done, _ = env._step(action, "Q")
            next_observation_enemy = env._step(enemy_action)

            # update q_table
            q_table = updateQtable(env, q_table, observation, action, reward, next_observation)
            total_reward += reward

            observation = next_observation
            observation_Enemy = next_observation_enemy

        a = np.array([episode + 1, total_reward])
        print(env.judVoL())
        if env.judVoL() == "Win_1":
            win1 += 1
        else:
            win2 += 1

        print(episode)

    # save q table
    with open('q_table_QL.csv', 'w') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerows(q_table)
"""
