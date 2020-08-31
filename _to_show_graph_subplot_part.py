import cv2
import numpy as np
import sys
import pandas as pd
import matplotlib.pylab as plt

# 아기 정하기
baby_num = 3
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


def show_graph(s, e, n):
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


    # p값 normalize
    _max = p.max()
    _min = p.min()
    _denom = _max - _min
    p = ((p - _min) / _denom) * max(x.max(), y.max(), z.max())

    # xyz값 normalize
    _max = x.max()
    _min = x.min()
    _denom = _max - _min
    x = ((x - _min) / _denom) * n
    _max = y.max()
    _min = y.min()
    _denom = _max - _min
    y = ((y - _min) / _denom) * n
    _max = z.max()
    _min = z.min()
    _denom = _max - _min
    z = ((z - _min) / _denom) * n


    #figure 생성
    fig = plt.figure(1, figsize=(35, 10))
    a = fig.add_subplot(6, 1, 1)
    b = fig.add_subplot(6, 1, 2)
    c = fig.add_subplot(6, 1, 3)
    d = fig.add_subplot(6, 1, 4)

    # hist
    h = fig.add_subplot(6, 1, 5)

    # hist
    corr = fig.add_subplot(6, 1, 6)

    # xticks 설정
    a.set_xticks(ticks)
    b.set_xticks(ticks)
    c.set_xticks(ticks)
    d.set_xticks(ticks)

    # grid 설정
    a.grid(True)
    b.grid(True)
    c.grid(True)
    d.grid(True)

    #a.bar(time[:10], p[:10])
    a.plot(time, p, label='Point Value')
    a.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    if not e == 0:
        a.set_xlim(s, e)

    b.plot(time, x, label= 'sensor_X')
    b.plot(time, y, label= 'sensor_Y')
    b.plot(time, z, label= 'sensor_Z')
    b.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    if not e == 0:
        b.set_xlim(s, e)

    c.plot(time, p, label='Point Value')
    c.plot(time, x, label= 'sensor_X')
    c.plot(time, y, label= 'sensor_Y')
    c.plot(time, z, label= 'sensor_Z')
    c.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    if not e == 0:
        c.set_xlim(s, e)

    d.plot(time, p, label='Point Value')
    d.plot(time, x, label='sensor_X')
    d.plot(time, y, label='sensor_Y')
    d.plot(time, z, label='sensor_Z')
    d.legend(loc='upper left', bbox_to_anchor=(1.0, 1.0))
    if not e == 0:
        d.set_xlim(s, e)
    d.set_ylim(0,(1.5*n))

    h.hist(df['point'], bins=int(len(df['point'])/5000))
    h.set_ylim(0,np.mean(df['point'])*2)

    #plt.savefig('baby'+str(baby_num+2)+'_part.png', bbox_inches='tight')
    plt.show()

show_graph(0, 0, 0.3)

# 0 -> 8, 1.5
# 1 -> 2, 1.5
# 2 -> 300, 1.5
# 3 -> 0.8, 1.5
# 4 -> 100, 1
# 5 -> 8, 1.5#

