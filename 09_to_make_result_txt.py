import cv2
import sys
import numpy as np
import pandas as pd
from pandas import DataFrame
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


def save_file(arr, name):
    np.set_printoptions(linewidth=np.inf)
    np.set_printoptions(threshold=np.inf)
    f = open(name, 'a')
    for i in np.arange(len(arr)):
        f.write(",".join(map(str, arr[i])))
        f.write('\n')
    f.close()


def make_result():
    f_name = 'baby' + str(baby_num + 2) + '_total.txt'
    file = '/home/lkw/PycharmProjects/newborn_video/' + f_name

    df = pd.read_csv(file, sep=',', header=None)
    df.columns = ['timeline', 'frame', 'point', 'x', 'y', 'z']
    t = df['timeline']
    f = df['frame']
    p = df['point']
    x = df['x']
    y = df['y']
    z = df['z']
    l = pd.Series(np.zeros((len(df)), dtype=int))
    result = pd.concat([t,f,p,x,y,z,l], axis=1)

    #save_file_name = 'baby' + str(baby_num + 2) + '_result.txt'
    #result.to_csv(save_file_name, index=False, header=None)


for i in np.arange(6):
    baby_num = i
    make_result()