#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyzbar.pyzbar import decode
from pyzbar.pyzbar import ZBarSymbol
import cv2
import numpy as np


def edit_contrast(image, gamma):
    """コントラクト調整"""
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
            init_pos = [[iv_list[size],iv_list[size + 1]],[iv_list[size + 2],iv_list[size + 3]]]
            del iv_list[size:]
            r.append(init_pos)
            r.append(iv_list)
            break
    return r
