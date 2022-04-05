import cv2
from cv2 import FILLED
import mediapipe as mp
import numpy as np
import mss
import keyboard
import time
import ctypes, sys
import mouse



mpPose = mp.solutions.pose
poses = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=10)
poseconStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)

sct = mss.mss()#mss截圖
top = 360
left = 480
width = 200
height = 200
monitor = {"top": top, "left": left, "width": width, "height": height}#截圖方框位置
istart = True

def is_admin():
    #檢測當前程式是不是管理員模式
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False
if is_admin():
    #Code of your program here        
    while True:
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
        if(mouse.is_pressed() & istart):
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            results = poses.process(image)
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
                        x=int((lm.x-0.5)*imgWide+20)
                        y=int((lm.y-0.5)*imgHeigh+20)
                        mouse.move(x, y, absolute=False, duration=0)
                        break
        image = cv2.resize(image,(0,0),fx=1.5,fy=1.5)
        cv2.putText(image,"Fps :"+str(int(1/(time.time()-t))),(1,30),cv2.FONT_HERSHEY_SIMPLEX,1,(204,255,0),2)
        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(1) & 0xFF == 27:
            break
else:
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)