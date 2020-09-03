import cv2
import threading
import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5 import QtTest
from PyQt5.QtGui import *

# 경로
path = [
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_2_F_d9_인큐베이터/captured_data_hospital_20200207_133526_인큐베이터/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_3/captured_data_hospital_20200207_161139/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_4_M_d2/captured_data_hospital_20200207_211837/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_5_M_d16/captured_data_hospital_20200210_163202/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_6_M_d3/captured_data_hospital_20200213_143500/',
    '/home/lkw/PycharmProjects/newborn_video/newborn_data/Baby_7_M_d4/captured_data_hospital_20200213_170925/']

data_start_num = ['202002071340', '202002071617', '202002072124', '202002101632', '202002131440', '202002131709']
date_end_num = ['202002071525', '202002071742', '202002072259', '202002101842', '202002131700', '202002131829']

# 사용할 변수들
baby_num = 0
extension = '.avi'

speed_V = 1.0
check_con = False
running = False
path_str = ''

start_frame = 0
end_frame = 0
cnt_frame = 0
video_index = 0
x_ticks = []

loop_cnt = 0
ischanged = False
waiting = False
isfirstSearch = True
isStop = False

form_class = uic.loadUiType("gui.ui")[0]


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.button_fast.clicked.connect(self.btn_fast)
        self.button_slow.clicked.connect(self.btn_slow)

        self.button_change.clicked.connect(self.btn_change)
        self.button_done.clicked.connect(self.btn_done)
        self.button_search.clicked.connect(self.btn_search)

        self.button_stop.clicked.connect(self.btn_stop)

        self.check_continue.stateChanged.connect(self.checking)

        self.combo_baby.addItem("-")
        self.combo_baby.addItem("2")
        self.combo_baby.addItem("3")
        self.combo_baby.addItem("4")
        self.combo_baby.addItem("5")
        self.combo_baby.addItem("6")
        self.combo_baby.addItem("7")
        self.combo_baby.activated[str].connect(self.combobox_Changed)
        self.combo_video.activated[str].connect(self.combobox_video_Changed)

        self.slider

    def combobox_Changed(self):
        global video_index
        global x_ticks

        if self.combo_baby.currentText() == '-':
            self.combo_video.clear()
            return

        global baby_num
        baby_num = int(self.combo_baby.currentText()) - 2

        temp = [f for f in os.listdir(path[baby_num]) if os.path.isfile(os.path.join(path[baby_num], f))]

        result = [s for s in temp if extension in s]
        result.sort()

        self.combo_video.clear()
        for i in result:
            self.combo_video.addItem(i)

        video_index = int(self.combo_video.currentIndex())
        f_name = 'baby' + str(baby_num + 2) + '_ticks.txt'
        file = '/home/lkw/PycharmProjects/newborn_video/' + f_name
        df_tick = pd.read_csv(file, sep=',', header=None)
        df_tick.columns = ['xticks']
        x_ticks = df_tick['xticks']

    def combobox_video_Changed(self):
        global x_ticks
        global video_index

        video_index = int(self.combo_video.currentIndex())

        f_name = 'baby' + str(baby_num + 2) + '_ticks.txt'
        file = '/home/lkw/PycharmProjects/newborn_video/' + f_name
        df_tick = pd.read_csv(file, sep=',', header=None)
        df_tick.columns = ['xticks']
        x_ticks = df_tick['xticks']

    def btn_stop(self):
        global running
        global ischanged
        global loop_cnt
        global start_frame
        global isfirstSearch
        global isStop

        isStop = True
        isfirstSearch = False
        running = False
        #ischanged = True
        loop_cnt = int(start_frame/120) + 1

        self.slider.setValue(0)
        self.label_view.clear()
        self.label_view.setText("이 곳에서 영상이 출력됩니다.")

    def btn_fast(self):
        global speed_V

        if speed_V < 8:
            speed_V *= 2
            self.speed.setText('x' + str(speed_V))

    def btn_slow(self):
        global speed_V

        if speed_V > 0.5:
            speed_V /= 2
            self.speed.setText('x' + str(speed_V))

    def btn_change(self):
        global ischanged

        ischanged = True
        print("change")

    def btn_done(self):
        print("done")

    def btn_search(self):
        print("search")
        global baby_num
        global path_str
        global start_frame
        global end_frame
        global loop_cnt
        global running
        global waiting
        global isStop

        isStop = False

        if running:
            print("not yet playing")
            return
        elif waiting:
            print("not yet changed")
            return

        path_str = path[baby_num] + str(self.combo_video.currentText())
        start_frame = int(self.range_start.toPlainText())
        end_frame = int(self.range_end.toPlainText())

        # 슬라이드 바
        self.slider.setMinimum(start_frame)
        self.slider.setMaximum(end_frame)
        self.slider.setValue(start_frame)

        loop_cnt = int(start_frame/120) + 1
        start()

    def checking(self):
        global check_con
        check_con = not check_con
        print(check_con)


def play(img, fps):
    global cnt_frame

    slider.setValue(cnt_frame)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    h, w, c = img.shape
    qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
    pixmap = QtGui.QPixmap.fromImage(qImg)
    label_view.setPixmap(pixmap)
    QtTest.QTest.qWait(fps / speed_V)

def run():
    global running
    global speed_V
    global path_str
    global cnt_frame
    global start_frame
    global end_frame
    global video_index
    global loop_cnt
    global ischanged
    global waiting
    global isfirstSearch
    global isStop

    if isfirstSearch:
        isfirstSearch = False
        show_graph(start_frame, end_frame)

    cap = cv2.VideoCapture(path_str)
    fps = cap.get(cv2.CAP_PROP_FPS)
    fps = int(1000 / fps)

    while running:
        ret, img = cap.read()
        if ret:
            cnt_frame += 1
            label_now.setText("현재 프레임 위치 : " + str(cnt_frame))
            label_state.setText(str(loop_cnt))

            if cnt_frame < start_frame:
                label_view.clear()
                if cnt_frame >= 120 + 30 * (loop_cnt - 1):
                    loop_cnt += 1
                continue
            elif cnt_frame >= end_frame:
                running = False
                slider.setValue(cnt_frame)
                label_view.clear()
                label_view.setText("이 곳에서 영상이 출력됩니다.")
                break
            else:
                if check_con:
                    play(img, fps)
                    if cnt_frame >= 120 + 30 * (loop_cnt-1):
                        loop_cnt += 1
                else:
                    play(img, fps)
                    if cnt_frame >= 120 + 30 * (loop_cnt-1):
                        loop_cnt += 1
                        while 1:
                            waiting = True
                            print('1')
                            print(isStop)
                            print(ischanged)
                            if isStop:
                                isStop = False
                                ischanged = False
                                waiting = False
                                cnt_frame = 0
                                cap.release()
                                return
                            elif ischanged:
                                ischanged = False
                                waiting = False

                                cnt_frame = 0
                                if start_frame < 30 * (loop_cnt-1):
                                    start_frame = 30 * (loop_cnt-1)
                                cap.release()
                                start()
                                return
        else:
            QtWidgets.QMessageBox.about(myWindow, "Error", "Cannot read frame.")
            print("cannot read frame.")
            break
    cnt_frame = 0
    isfirstSearch = False
    cap.release()

    print("Thread end.")


def start():
    global running
    running = True
    th = threading.Thread(target=run)
    th.daemon = True
    th.start()
    print("started..")


def stop():
    global running
    running = False
    print("stopped..")


def onExit():
    print("exit")
    stop()


def show_graph(s, e):
    global tt
    f_name = 'baby' + str(baby_num + 2) + '_total.txt'
    file = '/home/lkw/PycharmProjects/newborn_video/' + f_name
    df = pd.read_csv(file, sep=',', header=None)
    df.columns = ['timeline', 'frame', 'point', 'x', 'y', 'z']
    time = np.arange(len(df))
    p = df['point']

    # 콤보박스로 선택한 비디오의 시간축을 0~198000... 에서 각각 0~9000 으로 접근할 수 있도록 만들기
    if not (x_ticks[video_index] == x_ticks[len(x_ticks) - 1]):
        tt = time[x_ticks[video_index]:x_ticks[video_index + 1] - 1]
        pp = p[x_ticks[video_index]:x_ticks[video_index + 1] - 1]
    else:
        tt = time[x_ticks[video_index]:]
        pp = p[x_ticks[video_index]:]
    tt = tt - tt[0]

    tt_max = tt.max()
    tt_min = tt.min()
    ttt = np.round((tt - tt_min) / (tt_max - tt_min) * 9000)

    plt.figure(figsize=(9, 1))
    plt.plot(ttt, pp, label='Point Value')
    plt.xlim(s, e)
    # plt.ylim(0,max(pp[s:e]))   # 이걸 넣으면 짧은 컷 그래프가 크게 나옴(ylim값이 작아짐) 근데 기준이 매번 바뀜
    plt.savefig('frame_part.png', bbox_inches='tight')

    qPixmapVar = QPixmap()
    qPixmapVar.load('frame_part.png')
    label_video.setPixmap(qPixmapVar)


if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # WindowClass  인스턴스 생성
    myWindow = WindowClass()

    label_view = myWindow.label_view
    label_now = myWindow.label_now
    label_sensor = myWindow.label_sensor
    label_video = myWindow.label_video
    label_state = myWindow.label_state
    slider = myWindow.slider
    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
