
import gym
import requests
import numpy as np
import csv
import matplotlib.pyplot as plt
from collections import deque
import time
import threading
import datetime
from texttable import Texttable
import QLprocon2018 as Q
import mcl0917 as M
import linenotify
import sys

def Log(m,fm):
    fn = './log/' + fm + '.txt'
    f = open(fn,'a')
    f.write(m)
    f.close()

def saveImage():
    plt.subplot(2,2,1)
    plt.plot(s3, 'r', label="QL")
    plt.plot(s6, 'b', label="MCM")
    plt.xlim(0, episode)
    plt.ylim(-500, 500)
    plt.xlabel("epoch")
    plt.ylabel("total point")
    plt.legend(loc='lower right')
    plt.subplot(2,2,3)
    plt.plot(s1, 'r', label="QL")
    plt.plot(s4, 'b', label="MCM")
    plt.xlim(0, episode)
    plt.ylim(-500, 500)
    plt.xlabel("epoch")
    plt.ylabel("tilepoint")
    plt.legend(loc='lower right')
    plt.subplot(2,2,4)
    plt.plot(s2, 'r', label="QL")
    plt.plot(s5, 'b', label="MCM")
    plt.xlim(0, episode)
    plt.ylim(-500, 500)
    plt.xlabel("epoch")
    plt.ylabel("fieldpoint")
    plt.legend(loc='lower right')
    plt.savefig('./result/result_point.png')

    plt.figure()
    plt.plot(f_rr, 'r', label="QL")
    plt.plot(e_rr, 'b', label="MCM")
    plt.xlim(0, episode)
    plt.ylim(-500, 500)
    plt.xlabel("epoch")
    plt.ylabel("reward")
    plt.legend(loc='lower right')
    plt.savefig('./result/result_reward.png')

def notify(num_episode,Win1,Win2,s3,s6):#,s3,s4,s5,s6):
    #table = Texttable()
    ended_mess = "Learning was successful!\n"
    epoch_mess = "epoch is " + str(num_episode) + "\n"
    result_mess = "How many times did QL win?\n" + str(Win1) + "\n" + "How many times did MCM win?\n" + str(Win2) + "\n"
    finaltotalPoint_mess = "{total point}\n" + "[final point]\n" + "QL is " + str(s3[num_episode-1]) + "\n" + "MCM is " + str(s6[num_episode-1]) + "\n"
    maxtotalPoint_mess = "[max point]\n" + "QL is " + str(max(s3)) + "\n" + "MCM is " + str(max(s6)) + "\n"
    mintotalPoint_mess = "[min point]\n" + "QL is " + str(min(s3)) + "\n" + "MCM is " + str(min(s6)) + "\n"
    """
    finaltilePoint_mess = "{tile point}\n" + "[final point]\n" + "QL is " + str(s1[num_episode-1]) + "\n" + "MCM is " + str(s4[num_episode-1]) + "\n"
    maxtilePoint_mess = "[max point]\n" + "QL is " + str(max(s1)) + "\n" + "MCM is " + str(max(s4)) + "\n"
    mintilePoint_mess = "[min point]\n" + "QL is " + str(min(s1)) + "\n" + "MCM is " + str(min(s4)) + "\n"
    finalpanelPoint_mess = "{panel point}\n" + "[final point]\n" + "QL is " + str(s2[num_episode-1]) + "\n" + "MCM is " + str(s2[num_episode-1]) + "\n"
    maxpanelPoint_mess = "[max point]\n" + "QL is " + str(max(s2)) + "\n" + "MCM is " + str(max(s5)) + "\n"
    minpanelPoint_mess = "[min point]\n" + "QL is " + str(min(s2)) + "\n" + "MCM is " + str(min(s5)) + "\n"
    """
    mess = ended_mess + epoch_mess + result_mess + finaltotalPoint_mess + maxtotalPoint_mess + mintotalPoint_mess #+ finaltilePoint_mess + maxtilePoint_mess + mintilePoint_mess + finalpanelPoint_mess + maxpanelPoint_mess + minpanelPoint_mess
    fig_name = ['./result/result_point.png', './result/result_reward.png']
    #table.add_rows(['total','final','max','min'],['QL',str(s3[num_episode-1]),str(max(s3)),str(min(s3))],['MCM',str(s6[num_episode-1]),str(max(s6)),str(min(s6))])
    Log(m,fm)
    """
    linenotify.main_m(mess)
    for i in range(2):
        linenotify.main_f(fig_name[i],fig_name[i])
    """
# [] main processing
if __name__ == '__main__':
    # [] make environment
    now = datetime.datetime.now()
    fm = now.strftime("%Y%m%d_%H%M%S")
    m = "==================== start time is " + str(now) + ' ==================== \n'
    Log(m,fm)
    #linenotify.main_m(m)

    env = gym.make('procon18env-v8005')
    num_episode = 5000
    Win1 = 0
    Win2 = 0

    # read q tables from csv file
    q_table = Q.readQtable('QL')
    q_table_Enemy = Q.readQtable('MCM')
    f_rr = [] # 味方の各エピソードの報酬
    e_rr = [] # 敵の各エピソードの報酬
    f_r = []
    e_r = []
    s1 = []
    s2 = []
    s3 = []
    s4 = []
    s5 = []
    s6 = []

    try:
        for episode in range(num_episode):
            # choose initial position (5 or 6)
            choice = np.random.choice([0, 1])
            observation = env.reset(choice)
            terns = env.num_terns
            total_reward_f = 0
            total_reward_e = 0
            memory1 = M.Memory(terns)
            memory2 = M.Memory(terns)
            print("epoch is")
            print(episode)
            print("pattern is")
            print(choice)

            for i in range(terns):
                env.steps = i+1
                ob_f = env.getStatus(observation[0])
                ob_e = env.getStatus(observation[1])

                action_f = Q.getAction(env, q_table, ob_f, episode, choice) # array
                action_e = M.getAction(env, q_table_Enemy, ob_e, episode, choice)

                for i in range(2):
                    if action_f[i][2] == action_e[i][2]: # 移動先が被ったら停留
                        action_f[i][1] == "stay"
                        action_e[i][1] == "stay"

                next_observation, reward, done, _ = env.step(action_f,action_e,terns)
                # process (enemy_mcm)
                memory1.add((ob_e[0], action_e[0], reward[1][0]))
                memory2.add((ob_e[1], action_e[1], reward[1][1]))
                # process (friend_q)
                q_table = Q.updateQtable(env, q_table, observation[0], action_f, reward[0], next_observation[0])

                total_reward_f += (reward[0][0] + reward[0][1])
                total_reward_e += (reward[1][0] + reward[1][1])
                observation = next_observation

                # process (enemy_mcm)
                if done:
                    # update q_table_Enemy
                    q_table_Enemy = M.updateQtable(q_table_Enemy, memory1)
                    q_table_Enemy = M.updateQtable(q_table_Enemy, memory2)
                    break
            f_rr.append(total_reward_f)
            e_rr.append(total_reward_e)
            s = env.calcPoint()
            s3.append(s[0])
            s6.append(s[1])
            """
            s3.append(s[2])
            s4.append(s[3])
            s5.append(s[4])
            s6.append(s[5])
            """
            if env.judVoL() == "Win_1":
                f_r.append(1)
                e_r.append(-1)
                Win1 += 1
                print('Win1')
            else:
                f_r.append(-1)
                e_r.append(1)
                Win2 += 1
                print('Win2')

            if episode%500 == 0 and episode!=num_episode-1 :
                saveImage()
                now = datetime.datetime.now()
                m = "epoch is " + str(episode) + " now.\n" + "Win1 is " + str(Win1) + "\n" + "Win2 is " + str(Win2) + "\n" + "now time is " + str(now) + '\n'
                Log(m,fm)
                """
                linenotify.main_m(m)
                fig_name = ['./result/result_point.png', './result/result_reward.png']
                for i in range(2):
                    linenotify.main_f(fig_name[i],fig_name[i])
                """
            """
            plt.subplot(2,2,1)
            plt.plot(s3, 'r', label="QL")
            plt.plot(s6, 'b', label="MCM")
            plt.xlim(0, episode)
            plt.ylim(-500, 500)
            plt.xlabel("epoch")
            plt.ylabel("total point")
            plt.legend(loc='lower right')
            plt.subplot(2,2,3)
            plt.plot(s1, 'r', label="QL")
            plt.plot(s4, 'b', label="MCM")
            plt.xlim(0, episode)
            plt.ylim(-500, 500)
            plt.xlabel("epoch")
            plt.ylabel("tilepoint")
            plt.legend(loc='lower right')
            plt.subplot(2,2,4)
            plt.plot(s2, 'r', label="QL")
            plt.plot(s5, 'b', label="MCM")
            plt.xlim(0, episode)
            plt.ylim(-500, 500)
            plt.xlabel("epoch")
            plt.ylabel("fieldpoint")
            plt.legend(loc='lower right')
            if episode == num_episode - 1:
                plt.savefig('result_point.png')
            else:
                plt.pause(0.0001)
            """

        Q.writeQtable("QL", q_table)
        Q.writeQtable("MCM", q_table_Enemy)
        print("How many times did QL win?")
        print(Win1)
        print("How many times did MCM win?")
        print(Win2)
        """
        plt.figure()
        plt.plot(f_rr, 'r', label="QL")
        plt.plot(e_rr, 'b', label="MCM")
        plt.xlim(0, episode)
        plt.ylim(-500, 500)
        plt.xlabel("epoch")
        plt.ylabel("reward")
        plt.legend(loc='lower right')
        plt.savefig('result_reward.png')
        """
        saveImage()
        notify(num_episode,Win1,Win2,s3,s6)
        #notify(num_episode,Win1,Win2,s1,s2,s3,s4,s5,s6)
        now = datetime.datetime.now()
        m = "finished time is " + str(now)
        print(m)
        Log(m,fm)
        #linenotify.main_m(m)

    except:
        m = str(sys.exc_info())
        print(m)
        #linenotify.main_m(m)
        Q.writeQtable("QL", q_table)
        Q.writeQtable("MCM", q_table_Enemy)
        saveImage()
        #notify(num_episode,Win1,Win2,s3,s6)
        #notify(num_episode,Win1,Win2,s1,s2,s3,s4,s5,s6)
        now = datetime.datetime.now()
        m = "(error)finished time is " + str(now)
        Log(m,fm)
        #linenotify.main_m(m)
