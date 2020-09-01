import cv2
import numpy as np
import sys
import pandas as pd
import matplotlib.pylab as plt

# 아기 정하기
baby_num = 0
extension = '.avi'

# 경로 설정
path = [
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_2_F_d9_인큐베이터/captured_data_hospital_20200207_133526_인큐베이터/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_3/captured_data_hospital_20200207_161139/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_4_M_d2/captured_data_hospital_20200207_211837/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_5_M_d16/captured_data_hospital_20200210_163202/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_6_M_d3/captured_data_hospital_20200213_143500/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_7_M_d4/captured_data_hospital_20200213_170925/']

data_start_num = ['202002071340', '202002071617', '202002072124', '202002101632', '202002131440', '202002131709']
date_end_num = ['202002071525', '202002071742', '202002072259', '202002101842', '202002131700', '202002131829']


def show_all_graph():
    f_name = 'baby' + str(baby_num + 2) + '_total.txt'
    file = '/home/lkw/PycharmProjects/newborn_video/' + f_name

    df = pd.read_csv(file, sep=',', header=None)
    df.columns = ['timeline', 'frame', 'point', 'x', 'y', 'z']
    time = np.arange(len(df))
    p = df['point']
    x = df['x']
    y = df['y']
    z = df['z']

    ticks =[0]
    # xticks 설정
    # 1. cnt해서 자르기
    for i in np.arange(1, len(df)-1):
        if df['frame'][i] < df['frame'][i-1]:
            ticks = np.hstack((ticks, i))

    # 2. 넘어가는 해당 값 가져오기             -> 해당 시간은 구할 수 있는데 이걸 그래프로 표시를 못하겠다
    # non_ticks = []
    # for i in np.arange(1, len(df)-1):
    #    if df['frame'][i] > df['frame'][i-1]:
    #        non_ticks = np.hstack((non_ticks, i))
    # df = pd.read_csv(file, sep=',', skiprows=non_ticks, header=None)
    # df.columns = ['timeline', 'frame', 'point', 'x', 'y', 'z']
    # ticks = df['timeline']


    # p값 normalize
    #_max = p.max()
    #_min = p.min()
    #_denom = _max - _min
    #p = ((p - _min) / _denom) * max(x.max(), y.max(), z.max())


    ######
    plt.figure(1, figsize=(35, 5))
    plt.grid(True)
    plt.xticks(ticks)
    plt.plot(time, p)

    plt.figure(2, figsize=(35, 5))
    plt.grid(True)
    plt.xticks(ticks)
    plt.plot(time, x)
    plt.plot(time, y)
    plt.plot(time, z)
    plt.show()

show_all_graph()
