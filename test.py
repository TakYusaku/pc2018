
import gym
import requests
import numpy as np
import csv
import matplotlib.pyplot as plt
from collections import deque
import time
import threading
import QLprocon2018 as Q
import mcl0917 as M

# [] main processing
if __name__ == '__main__':
    # [] make environment
    env = gym.make('procon18env-v0')
    num_episode = 10

    is_learned = 0 #学習終了フラグ
    is_render = 0 #描画フラグ
    win1 = 0
    win2 = 0

    # read q tables from csv file
    q_table = Q.readQtable('QL')
    q_table_Enemy = Q.readQtable('MCM')
    f_rr = [] # 味方の各エピソードの報酬
    e_rr = [] # 敵の各エピソードの報酬
    f_r = []
    e_r = []

    for episode in range(num_episode):
        # choose initial position (5 or 6)
        choice = np.random.choice([0, 1])
        observation = env._reset(choice)
        terns = env.num_terns
        row = env.Row
        column = env.Column
        total_reward_f = 0
        total_reward_e = 0
        memory1 = M.Memory(terns)
        memory2 = M.Memory(terns)

        for i in range(terns):
            env.steps = i+1
            #ob_f = env.getStatus(observation[0])
            ob_e = env.getStatus(observation[1])

            action_f = Q.getAction(env, q_table, observation[0], episode) # array
            action_e = M.getAction(env, q_table_Enemy, observation[1], episode )

            for i in range(2):
                if action_f[i][2] == action_e[i][2]: # 移動先が被ったら停留
                    action_f[i][0] == 4
                    action_e[i][0] == 4

            next_observation, reward, done, _ = env._step(action_f,action_e)
            # process (enemy_mcm)
            memory1.add((ob_e[0], action_e[0], reward[1]))
            memory2.add((ob_e[1], action_e[1], reward[1]))
            # process (friend_q)
            q_table = Q.updateQtable(env, q_table, observation[0], action_f, reward[0], next_observation[0])

            total_reward_f += reward[0]
            total_reward_e += reward[1]
            observation = next_observation

            # process (enemy_mcm)
            if done:
                # update q_table_Enemy
                q_table_Enemy = M.updateQtable(q_table, memory1)
                q_table_Enemy = M.updateQtable(q_table, memory2)
                break
        f_rr.append(total_reward_f)
        e_rr.append(total_reward_e)
        if env.judVoL() == "Win_1":
            f_r.append(1)
            e_r.append(-1)
        else:
            f_r.append(-1)
            e_r.append(1)

    #plt.cla()
    plt.subplot(1,2,1)
    plt.plot(f_rr, 'r')
    plt.plot(e_rr, 'b')
    plt.xlim(0, episode)
    plt.ylim(min(f_rr) - 50, max(e_rr) + 50)
    plt.xlabel("epoch")
    plt.ylabel("reward")
    plt.subplot(1,2,2)
    plt.plot(f_r, 'r')
    plt.plot(e_r, 'b')
    plt.xlim(0, episode)
    plt.ylim(-3, 3)
    plt.xlabel("epoch")
    plt.ylabel("victory or defeat")
    plt.show()

    Q.writeQtable("QL", q_table)
    Q.writeQtable("MCM", q_table_Enemy)
