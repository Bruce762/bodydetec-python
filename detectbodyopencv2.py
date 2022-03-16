import cv2
import numpy as np
import mss
import keyboard
import win32api
import win32con
import time
sct = mss.mss()#mss截圖
top = 0
left = 0
width = 1200
height = 1000
monitor = {"top": top, "left": left, "width": width, "height": height}#截圖方框位置
faceCascade = cv2.CascadeClassifier("C:/python/opencv/haarcascade_fullbo.xml")
while True:
    t=time.time()
    image = np.array(sct.grab(monitor))#截圖
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
    imgHeigh = image.shape[0]
    imgWide = image.shape[1]
    faceRect = faceCascade.detectMultiScale(image, 1.09, 3)#(gray, 縮小倍數, 偵測次數)回傳正方形
    for (x, y, w, h) in faceRect:
        cv2.rectangle(image,(x, y), (x+w, y+h), (0, 255, 0),2)
    cv2.imshow('Pose', image)
    if cv2.waitKey(1) & 0xFF == 27:
        break