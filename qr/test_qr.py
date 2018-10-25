#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
import numpy as np
import json
import requests


def edit_contrast(image, gamma):
    look_up_table = [np.uint8(255.0 / (1 + np.exp(-gamma * (i - 128.) / 255.)))
        for i in range(256)]

    result_image = np.array([look_up_table[value]
                             for value in image.flat], dtype=np.uint8)
    result_image = result_image.reshape(image.shape)
    return result_image


#if __name__ == "__main__":
def Decode():
    capture = cv2.VideoCapture(0)
    if capture.isOpened() is False:
        raise("IO Error")
    r = []
    while True:
        ret, frame = capture.read()
        if ret == False:
            continue

        # グレースケール化してコントラクトを調整する
        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image = edit_contrast(gray_scale, 5)

        # 加工した画像からフレームQRコードを取得してデコードする
        codes = decode(image)

        if len(codes) > 0:
            f = codes[0][0].decode(encoding='utf-8').replace(":"," ")
            iv_list = [int(i) for i in f.split()]
            row = iv_list[0]
            column = iv_list[1]
            r.append([row,column])
            size = row * column
            del iv_list[0:2]
            init_pos1 = [iv_list[size],iv_list[size + 1]]
            init_pos2 = [iv_list[size + 2],iv_list[size + 3]]
            del iv_list[size:]
            r.append(init_pos1)
            r.append(init_pos2)
            r.append(iv_list)
            break
    return r

if __name__ == "__main__":
    field_info = Decode()
    if field_info[1][0] == field_info[2][0]:
        e_initPosition = [[field_info[0][0]-field_info[1][0],field_info[1][1]-1],[field_info[0][0]-field_info[2][0],field_info[2][1]-1]]
    elif field_info[1][1] == field_info[2][1]:
        e_initPosition = [[field_info[1][0]-1,field_info[0][1]-field_info[1][1]],[field_info[2][0]-1,field_info[0][1]-field_info[2][1]]]
    else:
        e_initPosition = [[field_info[1][0]-1,field_info[2][1]-1],[field_info[2][0]-1,field_info[1][1]-1]]
    info = {
        "fieldSize":field_info[0],
        "f_initPosition":[[field_info[1][0]-1,field_info[1][1]-1],[field_info[2][0]-1,field_info[2][1]-1]],
        "e_initPosition":e_initPosition,
        "PointField":field_info[3]
    }
    #try:
    response = requests.post('http://localhost:8001/init', data=info)
    #except:
