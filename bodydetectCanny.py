import cv2
from cv2 import FILLED
import mediapipe as mp
import numpy as np
import mss
import keyboard
import win32api
import win32con
import time

mpPose = mp.solutions.pose
poses = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=10)
poseconStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)

sct = mss.mss()#mss截圖
top = 360
left = 480
width = 350
height = 350
monitor = {"top": top, "left": left, "width": width, "height": height}#截圖方框位置

while True:
    t=time.time()
    image = np.array(sct.grab(monitor))#截圖
    imgHeigh = image.shape[0]
    imgWide = image.shape[1]
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    results = poses.process(image)
    image = cv2.Canny(image, 270,300)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.pose_landmarks:  
        mpDraw.draw_landmarks(image, results.pose_landmarks, mpPose.POSE_CONNECTIONS, poseLmsStyle, poseconStyle)
        for i, lm in enumerate(results.pose_landmarks.landmark):
            if i == 0 and lm:
                xPos = lm.x* imgWide
                yPos = lm.y* imgHeigh
                xPos = int(xPos)
                yPos = int(yPos)
                image = cv2.circle(image, (xPos,yPos), 4, (255, 0, 0), FILLED)
                if keyboard.is_pressed("v"):
                    x=int((lm.x-0.5)*imgWide)
                    y=int((lm.y-0.5)*imgHeigh)
                    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
                break
    image = cv2.resize(image,(0,0),fx=1.5,fy=1.5)
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break