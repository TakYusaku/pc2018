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


if __name__ == "__main__":
    capture = cv2.VideoCapture(0)
    if capture.isOpened() is False:
        raise("IO Error")

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
            for code in codes:
                print(code)
