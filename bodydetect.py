import imghdr
import time

import cv2
import keyboard
import mediapipe as mp
import mss
import numpy as np
import win32api
import win32con
from cv2 import FILLED
from pynput.mouse import Listener

mpPose = mp.solutions.pose
poses = mpPose.Pose(static_image_mode=True, model_complexity = 0, enable_segmentation = True, smooth_landmarks = False, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils
poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=10)
poseconStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)
sct = mss.mss()#mss截圖
istart = True
iniM_Mouse=win32api.GetKeyState(0x04)
isMpress = False
movespeed = 1
#detectTime = 0
click=False
centerL = 0
centerT = 0
def clicked(x, y, button, is_press):
    if is_press:
        global click,centerL,centerT
        centerL=x
        centerT=y
        click=True

listener = Listener(on_click=clicked)
time.sleep(4)
print("detection start")
listener.start()
while True:
    if click:
        listener.stop()
        print("successfully")
        break

width = 400
height = 400
left = centerL - (width/2)
top = centerT - (height/2)
left = int(left)
top = int(top)
monitor = {"top": top, "left": left, "width": width, "height": height}#截圖方框位置

while True:
    m = win32api.GetKeyState(0x04)#取得滑鼠中鍵，按下時值為-128
    if m<0:
        iniM_Mouse = m
        isMpress = True
    elif m != iniM_Mouse and m>=0:
        iniM_Mouse = m
        isMpress = False
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
        #detectTime = 0

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
            BodyMiddleX = []
            BodyMiddleY = []
            for i, lm in enumerate(results.pose_landmarks.landmark):
                if i == 11 and lm:
                    BodyMiddleX.append(lm.x)
                    BodyMiddleY.append(lm.y)
                elif i == 12 and lm:
                    BodyMiddleX.append(lm.x)
                    BodyMiddleY.append(lm.y)
                elif i == 23 and lm:
                    BodyMiddleX.append(lm.x)
                    BodyMiddleY.append(lm.y)
                elif i == 24 and lm:
                    xPos = (lm.x+BodyMiddleX[0]+BodyMiddleX[1]+BodyMiddleX[2])*0.25* imgWide
                    yPos = (lm.y+BodyMiddleY[0]+BodyMiddleY[1]+BodyMiddleY[2])*0.25* imgHeigh
                    x=int((xPos-0.5*imgWide)*movespeed)
                    y=int((yPos-0.5*imgHeigh)*movespeed)
                    xPos = int(xPos)
                    yPos = int(yPos)
                    image = cv2.circle(image, (xPos,yPos), 4, (255, 0, 0), FILLED)
                    print(x)
                    print(y)
                    if isMpress:
                        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0) 
                        #detectTime+=1
                    #if detectTime>=10:
                        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
                    break
    image = cv2.resize(image,(0,0),fx=1,fy=1)
    cv2.putText(image,"Fps :"+str(int(1/(time.time()-t))),(1,30),cv2.FONT_HERSHEY_SIMPLEX,1,(204,255,0),2)
    cv2.imshow('MediaPipe Pose', image)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break
