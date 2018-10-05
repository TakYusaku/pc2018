import numpy as np
import matplotlib.pyplot as plt

f_rr = []
e_rr = []
f_r = []
e_r = []

f_rrr = 0
e_rrr = 10
f = 5
e = 0

for episode in range(100):
    f_rrr += 2
    f_rr.append(f_rrr)
    e_rrr *= 2
    e_rr.append(e_rrr)
    f += 1
    f_r.append(f)
    e -= 1
    e_r.append(e)

    plt.cla()
    plt.subplot(1,2,1)
    plt.plot(f_rr, 'r')
    plt.plot(e_rr, 'b')
    plt.xlim(0, episode)
    plt.ylim(min(e_r) - 5,max(e_rr) + 5)
    plt.xlabel("epoch")
    plt.ylabel("reward")
    plt.subplot(1,2,2)
    plt.plot(f_r, 'r')
    plt.plot(e_r, 'b')
    plt.xlim(0, episode)
    plt.ylim(-3, 3)
    plt.xlabel("epoch")
    plt.ylabel("victory or defeat")
    plt.pause(1)
