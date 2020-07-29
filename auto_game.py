# -*- coding:utf-8 -*-
# @author：LuffyLSX
# @version：1.0
# @update time：2019/8/31

import os
import time
import cv2
import random


adbExe = '%LOCALAPPDATA%\\Android\\sdk\\platform-tools\\adb.exe'

def connect():
    try:
        os.system(adbExe+' connect 127.0.0.1:7555')
    except:
        print('连接失败')


def click(x, y):
    xr = random.randint(-2, 2)
    yr = random.randint(-2, 2)
    os.system(adbExe+' shell input tap %s %s' % (x+xr, y+yr))


def screenshot():
    path = os.path.abspath('.') + '\images'
    os.system(adbExe+' shell screencap /data/screen.png')
    os.system(adbExe+' pull /data/screen.png %s' % path)


def resize_img(img_path):
    img1 = cv2.imread(img_path, 0)
    img2 = cv2.imread('images/screen.png', 0)
    height, width = img1.shape[:2]
    ratio = 2560 / img2.shape[1]
    size = (int(width/ratio), int(height/ratio))
    return cv2.resize(img1, size, interpolation=cv2.INTER_AREA)


def Image_to_position(image, m=0):
    image_path = 'images/' + str(image) + '.png'
    screen = cv2.imread('images/screen.png', 0)
    # template = cv2.imread(image_path, 0)
    template = resize_img(image_path)
    methods = [cv2.TM_CCOEFF_NORMED, cv2.TM_SQDIFF_NORMED, cv2.TM_CCORR_NORMED]
    image_x, image_y = template.shape[:2]
    result = cv2.matchTemplate(screen, template, methods[m])
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print(max_val)
    if max_val > 0.8:
        global center
        center = (max_loc[0] + image_y / 2, max_loc[1] + image_x / 2)
        print(center)
        return center
    else:
        return False


def run(n):
    images = ['start-go1', 'start-go2', 'end', 'level up']
    round = 0
    # Image_to_position('start-go1')
    # time.sleep(2)
    # Image_to_position('start-go2')
    # while not Image_to_position('end'):
    #     time.sleep(5)
    while True:
        time.sleep(10.0)
        screenshot()
        now = ''
        for image in images:
            if Image_to_position(image, m=0) != False:
                print(image)
                now = image
                tr = random.random()
                time.sleep(3.0+tr)
                click(center[0], center[1])

        if now == 'end':
            tr = random.random()
            time.sleep(3.0+tr)
            round = round + 1
            if round >= n:
                break


if __name__ == '__main__':
    connect()
    '''for i in range(int(input('输入刷图次数' + '\n'))):
        run()
        time.sleep(3)'''
    run(int(input('输入刷图次数' + '\n')))
    os.system(adbExe+' kill-server')
