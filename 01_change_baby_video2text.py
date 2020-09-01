import cv2
import numpy as np
import sys
import matplotlib.pylab as plt

# 텍스트화 시킬 아기 정하기
baby_num = 0
extension = '.avi'

# 사용할 변수들


# 경로 설정
path = [
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_2_F_d9_인큐베이터/captured_data_hospital_20200207_133526_인큐베이터/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_3/captured_data_hospital_20200207_161139/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_4_M_d2/captured_data_hospital_20200207_211837/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_5_M_d16/captured_data_hospital_20200210_163202/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_6_M_d3/captured_data_hospital_20200213_143500/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_7_M_d4/captured_data_hospital_20200213_170925/']

data_start_num = ['202002071340', '202002071617', '202002072124', '202002101632', '202002131640', '202002131709']
date_end_num = ['202002071525', '202002071742', '202002072259', '202002101842', '202002131700', '202002131829']


def save_file(arr, name):
    np.set_printoptions(linewidth=np.inf)
    np.set_printoptions(threshold=np.inf)
    f = open(name, 'a')
    for i in np.arange(len(arr)):
        f.write(",".join(map(str, arr[i])))
        f.write('\n')
    f.close()


# 요한이의 센서 txt의 경로를 받아오면, 해당 txt의 시간과 프레임, x, y,z 값을 반환
# 요한이의 센서 txt의 주소를 받아오면, 해당 txt의 시간과 프레임, x, y,z 값을 반환
def read_sensor_txt(txt_str):
    with open(txt_str) as file:
        timeline = []
        frameline = []
        x_val = []
        y_val = []
        z_val = []
        numbers = []
        isfirst = True

        lines = file.readlines()
        for line in lines:
            numbers.append(line.split())

        for i in np.arange(len(numbers)):
            if isfirst:
                isfirst = False
                timeline = numbers[i][0][:8]
                frameline = numbers[i][1][:]
                x_val = numbers[i][2][:]
                y_val = numbers[i][3][:]
                z_val = numbers[i][4][:]
            else:
                timeline = np.vstack((timeline, numbers[i][0][:8]))
                frameline = np.vstack((frameline, numbers[i][1][:]))
                x_val = np.vstack((x_val, numbers[i][2][:]))
                y_val = np.vstack((y_val, numbers[i][3][:]))
                z_val = np.vstack((z_val, numbers[i][4][:]))

    return timeline, frameline, x_val, y_val, z_val


# video 를 읽어와서 MOG 방식으로
# video_str = path[baby_num] + 'video_' + str(data_start_num[baby_num]) + extension
def read_video(video_str):
    frame_val = []
    point_val = []
    isfirst = True
    frame_cnt = 0

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(noiseSigma=8)
    cap = cv2.VideoCapture(video_str)

    while 1:
        ret, frame = cap.read()
        if ret:
            frame_cnt += 1
            fgmask = fgbg.apply(frame)

            nzeros = np.count_nonzero(fgmask)

            cv2.imshow('frame', frame)
            cv2.imshow('masked', fgmask)
            cv2.waitKey(1)

            if isfirst:
                isfirst = False
                frame_val = frame_cnt
                point_val = nzeros
            else:
                point_val = np.vstack((point_val, nzeros))
                frame_val = np.vstack((frame_val, frame_cnt))

        else:
            cap.release()
            cv2.destroyAllWindows()
            break


    return frame_val, point_val


# 한 baby의 전체 영상 읽어서 txt화 시키기
# video_str = path[baby_num] + 'video_' + str(data_start_num[baby_num]) + extension
def read_video_all():
    result = []
    isfirst = True
    date = int(data_start_num[baby_num])

    while 1:
        if date > int(date_end_num[baby_num]):
            break
        print(date)

        video_str = path[baby_num] + 'video_' + str(date) + extension

        # video 읽기
        F, P = read_video(video_str)

        # 읽은 값 병합시키기
        temp = np.hstack((F, P))
        if isfirst:
            isfirst = False
            result = temp
        else:
            result = np.vstack((result, temp))

        # 다음 파일 이름 구하기
        date += 5
        if int(str(date)[10:]) >= 60:
            date += 100
            date -= 60

    # 파일 내보내기
    #file_name = 'baby' + str(baby_num + 2) + '_video.txt'
    #save_file(result, file_name)

    return result


R = read_video_all()