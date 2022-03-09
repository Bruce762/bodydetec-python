from cgi import print_arguments
from pydoc import ErrorDuringImport
from urllib.parse import ParseResultBytes
import cv2
from cv2 import FILLED
import mediapipe as mp
import pyscreenshot as ImageGrab
import numpy as np
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose
# For webcam input:
i=0
with mp_pose.Pose(
    
    min_detection_confidence=0.2,
    min_tracking_confidence=0.2) as pose:
  while True:
    image = pyautogui.screenshot(region=[0,0,1000,1000]) # x,y,w,h
    image = np.array(image)
    image = cv2.resize(image,(0,0),fx=0.5,fy=0.5)
    imgHeigh = image.shape[0]
    imgWide = image.shape[1]
    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    '''
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    '''
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
        print(i)
        print(lm)
        if i == 0 and lm:
          print(lm.x)
          xPos = lm.x* imgWide
          yPos = lm.y* imgHeigh
          print(xPos)
          print(yPos)
          image = cv2.circle(image, (int(xPos), int(yPos)), 4, (255, 0, 0), FILLED)
    cv2.imshow('MediaPipe Pose', image)
    if cv2.waitKey(1) & 0xFF == 27:
      break