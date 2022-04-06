import cv2
from cv2 import FILLED
import mediapipe as mp
import numpy as np
import mss
import keyboard
import time
import ctypes, sys
import mouse
import win32api
import pydirectinput
import pyautogui
import win32con

mpPose = mp.solutions.pose
poses = mpPose.Pose(static_image_mode=True, model_complexity = 0, enable_segmentation = True, smooth_landmarks = False, min_detection_confidence=0.4)
mpDraw = mp.solutions.drawing_utils
poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=10)
poseconStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)
sct = mss.mss()#mss截圖
centerL = 800
centerT = 478
width = 300
height = 300
left = centerL - (width/2)
top = centerT - (height/2)
left = int(left)
top = int(top)
monitor = {"top": top, "left": left, "width": width, "height": height}#截圖方框位置
istart = True
movespeed = 1.5

    #Code of your program here        
while True:
    mouseleft = win32api.GetKeyState(0x02)#取得滑鼠左鍵，按下時值為-128
    
    if(keyboard.is_pressed('o')):
        istart = True
        print("mode : open")

    if(keyboard.is_pressed('p')):
        istart = False
        print("mode : close")

    t=time.time()
    image = np.array(sct.grab(monitor))#截圖
    imgHeigh = image.shape[0]
    imgWide = image.shape[1]

    if(istart):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = poses.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:  
            mpDraw.draw_landmarks(image, results.pose_landmarks, mpPose.POSE_CONNECTIONS, poseLmsStyle, poseconStyle)
            
            for i, lm in enumerate(results.pose_landmarks.landmark):
                
                if i == 11 and lm:
                    leftlm = lm.x

                if i == 12 and lm:
                    xPos = (lm.x+leftlm)*0.5* imgWide
                    yPos = lm.y* imgHeigh
                    xPos = int(xPos)
                    yPos = int(yPos)
                    image = cv2.circle(image, (xPos,yPos), 4, (255, 0, 0), FILLED)
                    x=int(((lm.x+leftlm)*0.5-0.5)*imgWide*movespeed)
                    y=int((lm.y-0.5)*imgHeigh*movespeed)
                    
                    if(mouseleft<0):
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
                    break
    image = cv2.resize(image,(0,0),fx=1,fy=1)
    cv2.putText(image,"Fps :"+str(int(1/(time.time()-t))),(1,30),cv2.FONT_HERSHEY_SIMPLEX,1,(204,255,0),2)
    cv2.imshow('MediaPipe Pose', image)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break