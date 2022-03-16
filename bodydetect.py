from cgi import print_arguments
from pickle import TRUE
import cv2
from cv2 import FILLED
import mediapipe as mp
import numpy as np
#import pyautogui
import mss
import keyboard
import win32api
import win32con
import time
#pyautogui.FAILSAFE = True
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# For webcam input:
sct = mss.mss()#mss截圖
top = 360
left = 480
width = 300
height = 300
monitor = {"top": top, "left": left, "width": width, "height": height}#截圖方框位置
with mp_pose.Pose(
    min_detection_confidence=0.6,
    min_tracking_confidence=0.6) as pose:
  while True:
    t=time.time()
    image = np.array(sct.grab(monitor))#截圖
    imgHeigh = image.shape[0]
    imgWide = image.shape[1]
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    '''
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    '''
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    results = pose.process(image)
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    #print(results.pose_landmarks)
    """
    if i==0 and results.pose_landmarks:
      print(results.pose_landmarks)
      i=1
    """
    if results.pose_landmarks:  
      for i, lm in enumerate(results.pose_landmarks.landmark):
        #print(i)
        #print(lm)
        #lm.x是倍數
        if i == 0 and lm:
          #print(lm.x)
          xPos = lm.x* imgWide
          yPos = lm.y* imgHeigh
          xPos = int(xPos)
          yPos = int(yPos)
          image = cv2.circle(image, (xPos,yPos), 4, (255, 0, 0), FILLED)
          if keyboard.is_pressed("v"):
            x=int((lm.x-0.5)*imgWide)
            y=int((lm.y-0.5)*imgHeigh)
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
            #win32api.SetCursorPos(((left+xPos*2),(top+yPos*2)))
            #pyautogui.moveTo((left+xPos*2),(top+yPos*2),duration=0.1)
          break
    image = cv2.resize(image,(0,0),fx=1.5,fy=1.5)
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(1) & 0xFF == 27:
      break