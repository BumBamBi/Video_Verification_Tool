import cv2
import numpy as np
import matplotlib.pylab as plt

# 텍스트화 시킬 아기 정하기
baby_num = 0
extension = '.avi'

# 사용할 변수들
isfirstbaby = True
tracker = 0

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


def check_roi(img):
    global tracker
    # initialize tracker
    OPENCV_OBJECT_TRACKERS = {
        "csrt": cv2.TrackerCSRT_create                  # 차별적 상관관계 필터를 이용.느리지만 높은정확도
        # ,"kcf": cv2.TrackerKCF_create,                # 커널화된 상관관계 필터와 수학적 특징 사용. 정확도와 속도가 MIL 보다 좋음 -> 사용 추천
        # "tld": cv2.TrackerTLD_create,                 # 추적/학습/탐지 를 이용하여 추적 -> 잘못학습하면..
        # "boosting": cv2.TrackerBoosting_create,       # 너무 오래전 알고리즘 -> 쓸 필요 x
        # "mil": cv2.TrackerMIL_create,                 # Multiple Instance Learning 사용. KCF의 하위버젼 -> 쓸 필요x
        # "medianflow": cv2.TrackerMedianFlow_create,   # 동작이 작고, 예측 가능하면 잘 작동함. -> 조건이 많이 붙음
        # "mosse": cv2.TrackerMOSSE_create              # 빠르고 나름 괜찮은 정확도천 그러나 성능에서 다른 추척기에 비해 뒤쳐지는 편
    }

    tracker = OPENCV_OBJECT_TRACKERS['csrt']()

    cv2.namedWindow('Select Window')
    cv2.imshow('Select Window', img)

    # select ROI
    rect = cv2.selectROI('Select Window', img, fromCenter=False, showCrosshair=True)
    cv2.destroyWindow('Select Window')

    # initialize tracker
    tracker.init(img, rect)

    global first_roi
    first_roi = rect

    return tracker


def tracking(img, mask):
    global tracker
    global first_roi
    global changed
    global pre_left
    global pre_top
    global pre_w
    global pre_h
    # update tracker and get position from new frame
    success, box = tracker.update(img)
    left, top, w, h = [int(v) for v in box]

    if left <= 0:
        tracker = cv2.TrackerCSRT_create()
        tracker.init(img, first_roi)

        left = pre_left
        top = pre_top
        w = pre_w
        h = pre_h

    else:
        pre_left = left
        pre_top = top
        pre_w = w
        pre_h = h

    center_x = left + w / 2
    center_y = top + h / 2

    w = first_roi[2]
    h = first_roi[3]

    m_left = center_x - w / 2
    m_top = center_y - h / 2

    m_right = left + w
    m_bottom = top + h

    pt1 = (int(m_left), int(m_top))
    pt2 = (int(m_right), int(m_bottom))

    mask = cv2.rectangle(mask, pt1, pt2, (255, 255, 255), -1)

    # visualize
    cv2.rectangle(img, pt1, pt2, (255, 255, 255), 3)

    return mask


# video 를 읽어와서 MOG 방식으로
# video_str = path[baby_num] + 'video_' + str(data_start_num[baby_num]) + extension
def read_video(video_str):
    global isfirstbaby
    global tracker
    frame_val = []
    point_val = []

    isfirst = True
    frame_cnt = 0

    fgbg = cv2.bgsegm.createBackgroundSubtractorMOG(noiseSigma=8)
    cap = cv2.VideoCapture(video_str)

    while 1:
        ret, frame = cap.read()
        if ret:
            if not ret:
                break
            if cv2.waitKey(1) == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                break

            if isfirstbaby:
                isfirstbaby = False
                tracker = check_roi(frame)

            frame_cnt += 1
            fgmask = fgbg.apply(frame)
            mask_pre = np.zeros_like(fgmask)

            if isfirst:
                isfirst = False
                mask = tracking(frame, mask_pre)

                result = cv2.bitwise_and(fgmask, mask)
                nzeros = np.count_nonzero(result)

                frame_val = frame_cnt
                point_val = nzeros
            else:
                if frame_cnt % 5 == 0:
                    mask = tracking(frame, mask_pre)

                result = cv2.bitwise_and(fgmask, mask)
                nzeros = np.count_nonzero(result)

                frame_val = np.vstack((frame_val, frame_cnt))
                point_val = np.vstack((point_val, nzeros))

            cv2.imshow('Frame', frame)
            cv2.imshow('masked', fgmask)
            cv2.imshow('mask', mask)
            cv2.imshow('result', result)

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
        F, P, = read_video(video_str)

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