# bodydetec-python
a program that detect body on screen and auto aim by mouse

## bodydetect.py :
when click middle mouse, it will autoly move mouse  the target(aim) and press left mouse(shoot).

## bodydetect2.py :
when click right mouse, if just autoly move mouse the target(aim).<br>

## 介紹
此程式是為了輔助新手遊玩槍戰遊戲所開發。

**用法:**
啟動程式後先點入遊戲裡面，進去遊戲裡過4秒後點擊一下滑鼠左鍵(為了抓去要截圖的位置)，像是在圖一遊戲中點一下。程式就會自動判斷鼠標位置，並以鼠標中心往外延伸150px作為判斷區域。判斷區域像是圖二右上角。接著當遇到擊人時只需要點擊右鍵，準心就會自動移動到敵人身上。按p會關掉Ai偵測，按o可以開啟偵測。按下ESC鍵可以退出程式。

**圖一**

<img width="600" height="341" alt="image" src="https://github.com/user-attachments/assets/b823c5ce-3e24-4424-929c-10b50dcc7d50" />

**圖二**

<img width="885" height="549" alt="image" src="https://github.com/user-attachments/assets/7a6801da-e431-40f8-af06-4740197d9ec4" />

## 細節討論
### 流程圖
使用draw.io完成

![](https://i.imgur.com/zpEILjq.png)


### 滑鼠位置偵測

這段程式碼的功能是在偵測滑鼠的位置，當點一下左鍵後會傳回滑鼠位置當作程式偵測範圍。centerL與centerT分別是中心點的橫向與垂直座標，Listener(on_click=clicked) 負責回傳座標與滑鼠是否點擊。listener.start()開始偵測後while迴圈會重覆直到滑鼠左鍵被點擊，點擊後listener.stop()則會結束偵測，然後在centerL與centerT存下點擊時的座標。

```python=
from pynput.mouse import Listener
click = False
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
```

### 截圖

由於遊戲的畫面是由一幀接著一幀顯示螢幕上，所以我寫一個迴圈一直截圖，在一秒內多次截圖。而且會一直重複直到按下ESC鍵結束程式。截圖的部分經過我測試多組函示庫後，我發現mss函示庫最符合我的需求，其它像是pyautogui、win32api等函示庫不是截圖太慢就是操作時常失敗。由於在一秒之內可能需要盡可能截越多張圖，因此如果截圖耗費太多時間就會降低程式效率，原本偵測到的敵人可能就會跑走。



```python=
import mss
import numpy as np
sct = mss.mss()#mss截圖
while True:
    image = np.array(sct.grab(monitor))#截圖
    主程式
    if cv2.waitKey(1) & 0xFF == 27:#按下ESC
        break
```
### Ai判斷函式庫

使用一個Google開源的函示庫。這是他們的官方 https://google.github.io/mediapipe/solutions/pose ，裡面有範例，我刪掉用不到的部分保留需要用到的。Mediapipe有很多函式可以用，而mp.soluiton.pose是其中有關人物偵測。第9行cv2.cvtColor()把圖片轉換成RGB的格式，因為需要RGB的格式Ai才能處理。第10行poses.process()把image(圖片)經過處理後，以NamedTuple的方式存在landmark，像是下圖(取自官方)總共有32個點。
![](https://i.imgur.com/dbMomJk.png =400x230)
為了讓我們觀測到每個點的標示狀態，14行的mpDraw.draw_landmarks會在image上標出點與點之間的連線。poseLmsStyle決定圓點的顏色粗細，poseconStyle則是線。16行用enumerate幫每個點的landmark(NameTuple)編號。由於我設定瞄準的點是胸口，所以我取第11與第12個landmark裡面的x、y座標做平均。第31行把FPS偵數算出，方便我知道程式跑的速度。

```python= 
import mediapipe as mp
import numpy as np
import cv2
import time

mpPose = mp.solutions.pose
poses = mpPose.Pose(static_image_mode=True, model_complexity = 0, enable_segmentation = True, smooth_landmarks = False, min_detection_confidence=0.4)
mpDraw = mp.solutions.drawing_utils
poseLmsStyle = mpDraw.DrawingSpec(color=(0, 0, 255), thickness=10)
poseconStyle = mpDraw.DrawingSpec(color=(0, 255, 0), thickness=10)

while True:
    t=time.time()
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
                   
    image = cv2.resize(image,(0,0),fx=1,fy=1)
    cv2.putText(image,"Fps :"+str(int(1/(time.time()-t))),(1,30),cv2.FONT_HERSHEY_SIMPLEX,1,(204,255,0),2)
    cv2.imshow('MediaPipe Pose', image)
    
    if cv2.waitKey(1) & 0xFF == 27:
        break

```


### 瞄準偵測與移動

第4行我用win32api.GetKeyState()是取得滑鼠右鍵是否按壓，且按下時的值小於零。接著在14行只要判斷滑鼠右鍵被按下之後，就會用win32api.mouse_event()把滑鼠移動到指定的位置。第6行的keyboard.is_pressed('o')檢測鍵盤上的o有沒有備按下，我設定當按下時開起Ai偵測人的功能。而keyboard.is_pressed('p')就是當按下鍵盤p時關閉Ai偵測人的功能。
```python=
import keyboard
import win32api
import win32con
mouseleft = win32api.GetKeyState(0x02)#取得滑鼠右鍵，按下時值為-128
    
if(keyboard.is_pressed('o')):
    istart = True
    print("mode : open")

if(keyboard.is_pressed('p')):
    istart = False
    print("mode : close")

if(mouseleft<0):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y, 0, 0)
```

## 參考網站
https://www.youtube.com/watch?v=1gZ-KaWjhGY&t=369s
https://www.youtube.com/watch?v=brwgBf6VB0I
https://google.github.io/mediapipe/solutions/pose
https://www.youtube.com/watch?v=x4eeX7WJIuA&t=436s
https://www.youtube.com/watch?v=xjrykYpaBBM&t=428s
https://www.youtube.com/watch?v=zdMUJJKFdsU&t=2s
https://www.twblogs.net/a/5d651e4cbd9eee5327fe6a58
https://stackoverflow.com/questions/68842206/python-mss-screen-capture-target-specific-windows
https://stackoverflow.com/questions/61915912/how-can-i-make-the-cursor-move-in-game-using-python-ex-first-shooter-shooting
\.\.\.


