import requests
import numpy as np
import csv
import test_qr as qr


def getAction(cnt,q_table,pos):
    a = []
    c = cnt
    cnt_a = []
    observation = getStatus(pos)
    for i in range(2):
        x = np.argsort(q_table[observation[i]])[::-1]
        b = False
        while b!=True:
            data = [
              ('usr', i+1),
              ('d', gaStr(x[c[i]])),
            ]
            f = requests.post('http://localhost:8001/judgedirection', data = data).text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
            iv_list = [t for t in f.split()]
            u = [int(iv_list[0]),int(iv_list[1])]
            if iv_list[2] == "Error":
                c[i] += 1
            elif iv_list[2] == "is_panel":
                a.append(["remove", gaStr(x[c[i]]),u])
                b = True
                cnt_a.append(c[i]+1)
            else:
                a.append(["move", gaStr(x[c[i]]),u])
                b = True
                cnt_a.append(c[i]+1)
    return a,cnt_a

def re_getAction(cnt,q_table,pos,num):
    a = []
    c = cnt
    cnt_a = []
    observation = getStatus(pos)
    x = np.argsort(q_table[observation[num-1]])[::-1]
    b = False
    while b!=True:
        data = [
          ('usr', num),
          ('d', gaStr(x[c[num-1]])),
        ]
        f = requests.post('http://localhost:8001/judgedirection', data = data).text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
        iv_list = [i for i in f.split()]
        s = [int(iv_list[0]),int(iv_list[1])]
        if iv_list[2] == "Error":
            c[num-1] += 1
        elif iv_list[2] == "is_panel":
            a.append(["remove", gaStr(x[c[num-1]]),s])
            b = True
            cnt_a.append(c[num-1]+1)
        else:
            a.append(["move", gaStr(x[c[num-1]]),s])
            b = True
            cnt_a.append(c[num-1]+1)
    return a,cnt_a

def getStatus(observation):
    obs1 = observation[0]
    obs2 = observation[1]

    a =  np.array([obs1[1]*12 + obs1[0], obs2[1]*12 + obs2[0]])
    return a

def gaStr(action): # get action str // verified
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

def readQtable(type):
    fn = './result/q_table_' + type + '_1007.csv'
    with open(fn, 'r') as file:
        lst = list(csv.reader(file))
    a = []
    for i in range(144):
        a.append(list(map(float,lst[i])))
    q_table = np.array(a)

    return q_table

def getPosition(usr): #get position (array)  // verified
    data = [
      ('usr', usr),
    ]

    response = requests.post('http://localhost:8001/usrpoint', data=data)
    f = response.text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
    pos_array =[int(i) for i in f.split()]
    return pos_array


def getDirection(dir):
    if dir == "lu":
        return [-1,1]
    elif dir == "u":
        return [0,1]
    elif dir == "ru":
        return [1,1]
    elif dir == "l":
        return [-1,0]
    elif dir == "s":
        return [0,0]
    elif dir == "r":
        return [1,0]
    elif dir == "ld":
        return [-1,-1]
    elif dir == "d":
        return [0,-1]
    elif dir == "rd":
        return [1,-1]


if __name__ == '__main__':
    response = requests.get('http://localhost:8001/start')
    f = response.text
    print(" @#$@#$@#$@#$@#$@#$ game start @#$@#$@#$@#$@#$@#$")
    print(f)
    ###
    ff = f.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
    iv_list = [int(i) for i in ff.split()] #listing initial value
    num_terns = iv_list[0] #number of terns
    Row = iv_list[1] #row of field
    Column = iv_list[2]
    ###
    #######
    field = qr.Decode()
    info = {
        "fieldSize":field_info[0],
        "initPosition":field_info[1],
        "PointField":field_info[2]
    }
    response = requests.post('http://localhost:8001/init', data=info)
    #######
    q_table = readQtable("QL")


    print("tern is " + str(num_terns))

    for i in range(num_terns):
        cnt = [0,0]
        print(" ================== now tern is " + str(1 + i) + " ================== ")
        print(requests.post('http://localhost:8001/show').text)
        response = requests.post('http://localhost:8001/pointcalc').text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
        v = [int(i) for i in response.split()]
        print(v)
        u3_pos = getPosition(3)
        u3_ac = ""
        u3 = ""
        u4_ac = ""
        u4 = ""
        while True:
            u3_ac = input()
            if u3_ac == "move" or u3_ac == "remove":
                break
            else:
                print("incorrect!!")
        while True:
            u3 = input()
            if u3 == "lu" or u3 == "u" or u3 == "ru" or u3 == "l" or u3 == "s" or u3 == "r" or u3 == "ld" or u3 == "d" or u3 == "rd":
                break
            else:
                print("incorect!!")

        if u3_ac == "remove":
            np3 = u3_pos
        else:
            nd3 = getDirection(u3)
            np3 = [u3_pos[0] + nd3[0],u3_pos[1] + nd3[1]]

        u4_pos = getPosition(4)
        while True:
            u4_ac = input()
            if u4_ac == "move" or u4_ac == "remove":
                break
            else:
                print("incorrect!!")
        while True:
            u4 = input()
            if u4 == "lu" or u4 == "u" or u4 == "ru" or u4 == "l" or u4 == "s" or u4 == "r" or u4 == "ld" or u4 == "d" or u4 == "rd":
                break
            else:
                print("incorect!!")

        if u4_ac == "remove":
            np4 = u4_pos
        else:
            nd4 = getDirection(u4)
            np4 = [u4_pos[0] + nd4[0],u4_pos[1] + nd4[1]]

        pos = [getPosition(1),getPosition(2)]
        e_ac, cnt = getAction(cnt,q_table,pos)

        print("next enemy position is ")
        print(e_ac)

        if np3 == e_ac[0][2]:
            u3_ac = "stay"
            e_ac[0][0] = "stay"
            np3 = u3_pos
            e_ac[0][2] = pos[0]
        if np3 == e_ac[1][2]:
            u3_ac = "stay"
            e_ac[1][0] = "stay"
            np3 = u3_pos
            e_ac[1][2] = pos[1]
        if np4 == e_ac[0][2]:
            u4_ac = "stay"
            e_ac[0][0] = "stay"
            np4 = u4_pos
            e_ac[0][2] = pos[0]
        if np4 == e_ac[1][2]:
            u4_ac = "stay"
            e_ac[1][0] = "stay"
            np4 = u4_pos
            e_ac[1][2] = pos[1]


        if u3_ac == "remove":
            data = [
              ('usr', 3),
              ('d', u3)
            ]
            r3 = requests.post('http://localhost:8001/remove', data=data)
        elif u3_ac == "move":
            data = [
              ('usr', 3),
              ('d', u3)
            ]
            r3 = requests.post('http://localhost:8001/move', data=data)
        if u4_ac == "remove":
            data = [
              ('usr', 4),
              ('d', u4)
            ]
            r4 = requests.post('http://localhost:8001/remove', data=data)
        elif u4_ac == "move":
            data = [
              ('usr', 4),
              ('d', u4)
            ]
            r4 = requests.post('http://localhost:8001/move', data=data)
        if e_ac[0][0] == "remove":
            data = [
              ('usr', 1),
              ('d', e_ac[0][1])
            ]
            r1 = requests.post('http://localhost:8001/remove', data=data)
        elif e_ac[0][0] == "move":
            data = [
              ('usr', 1),
              ('d', e_ac[0][1])
            ]
            r1 = requests.post('http://localhost:8001/move', data=data)
        if e_ac[1][0] == "remove":
            data = [
              ('usr', 2),
              ('d', e_ac[1][1])
            ]
            r2 = requests.post('http://localhost:8001/remove', data=data)
        elif e_ac[1][0] == "move":
            data = [
              ('usr', 2),
              ('d', e_ac[1][1])
            ]
            r2 = requests.post('http://localhost:8001/move', data=data)

        if num_terns-1 == i:
            response = requests.post('http://localhost:8001/pointcalc').text.encode('utf-8').decode().replace("\n", " ").replace("  "," ")
            v = [int(i) for i in response.split()]
            print(v)
            if v[0] > v[1]:
                print("Win1")
            elif v[0] == v[1]:
                print("tie")
            elif v[0] < v[1]:
                print("Win!!!")
