# -*- encoding: utf-8 -*-
'''
@File    :   iflycode自动写代码.py
@Time    :   2023/12/07 15:20:26
@Author  :   YoungYuan 
@Contact :   young_yuan@hotmail.com
@License :   (C)Copyright 2022-2031, YoungYuan
'''

'''
此应用是利用iflycode自动生成的代码
prompt：
- 我要开发一个手势，控制写字的应用，大拇指和食指捏合实现绘制轨迹，并在屏幕上显示，请问有什么思路吗？
response:
- 好的。以下是详细的执行方案
    1.获取实时视频流：采用外置设备(比如摄像头、相机)来获得即时的视频流。可用opencv库的VideoCapture()函数进行获取。
    2.手部识别关键点监测：在每个画面进行手部重要点的识别。可以借助mediapipe软件库检查手部关键点。
    3.检测捏动手势：为侦测到捏动手势，需要判断两个指尖间的距离是否变化。可以通过numpy库来计算欧式距离，如果距离小于设定的阈值，就认为正在进行捏动的行为。
    4.生成轨迹点：在侦测到捏动手势时，需要制作轨迹点。首先要计算两个捏动指尖的中心坐标，然后将这个中心坐标加入到轨迹点的表单中。轨迹点的表单可以用一个数组或者队列来保存。
    5.画出轨迹：将轨迹点的表单画在屏幕上，形成连续的轨迹。可以使用opencv库来画图。当侦测不到手的时候，需要清除轨迹点。
    总的来说，如果我们想制作一个可以模拟类似于在空中手写的手指捏合轨迹追踪应用，我们将需要执行视频流抓取、手部识别关键点监测、捏合手势检测、轨迹点生成和轨迹绘制。在编码过程中，借助第三方库可极大缩短开发时间。
prompt：
- 那就用python开发，具体需要包含哪些功能模块呢？需要导入哪些工具包？
response:
- 好的，下面是凌空手写的手指捏合轨迹点跟踪的应用功能的实现步骤：
    1.打开摄像头进行实时视频流的捕获，并实时显示出来
    2.测量手部区域上的关键点和边缘，并呈现关键点
    3.描绘手指捏合时的轨迹点跟踪与显示
    实现这个功能，需要导入的包有cv2、mediapipe、numpy
    import cv2
    import mediapipe as mp
    import numpy as np

然后，将上述三个步骤粘贴到编辑器，自动完成
'''



import cv2
import mediapipe as mp
import numpy as np


# 打开摄像头进行实时视频流的捕获，并实时显示出来
def video_capture():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        exit()

    while True:
        ret, frame = cap.read()

        if not ret:
            print("无法接收帧(视频流已结束？)")
            break

        frame = cv2.flip(frame, 1)

        # 调用detect_and_draw_hand_landmarks函数
        hand_landmarks = detect_and_draw_hand_landmarks(frame)

        # 调用draw_palm_points函数
        draw_palm_points(frame, hand_landmarks)

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# 测量手部区域上的关键点和边缘，并呈现关键点


def detect_and_draw_hand_landmarks(frame):
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(static_image_mode=False,
                           max_num_hands=2,
                           min_detection_confidence=0.5)

    mp_drawing = mp.solutions.drawing_utils
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_image)

    hand_landmarks = None
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks)
    hands.close()
    return hand_landmarks


# 描绘手指捏合时的轨迹点跟踪与显示
def draw_palm_points(frame, hand_landmarks, history_palm_points=[]):
    if not hand_landmarks:
        history_palm_points.clear()
        return
    thumb_index = 4
    indexfinger_index = 8

    indexfinger_point = hand_landmarks.landmark[indexfinger_index]
    thumb_point = hand_landmarks.landmark[thumb_index]

    finger_distance = np.sqrt((thumb_point.x - indexfinger_point.x) ** 2
                              + (thumb_point.y - indexfinger_point.y) ** 2)
    if finger_distance < 0.1:
        palm_point = [int((thumb_point.x + indexfinger_point.x) * frame.shape[1] // 2),
                      int((thumb_point.y + indexfinger_point.y) * frame.shape[0] // 2)]
        history_palm_points.append(palm_point)

    if len(history_palm_points) < 2:
        pass
    else:
        for i in range(1, len(history_palm_points)):
            cv2.line(frame, tuple(history_palm_points[i-1][:2]), tuple(history_palm_points[i][:2]), (0, 0, 255), 5) 



# 调用video_capture函数
if __name__ == '__main__':
    video_capture()
