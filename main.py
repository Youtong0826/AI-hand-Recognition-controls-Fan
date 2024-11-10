import cv2
from mediapipe.python.solutions import hands
from requests import get
import math
from finger_type import *
from typing import overload
# 定義一個二維空間的座標類別 有x, y兩種屬性
class Position2d:
    """
    args:   
        `x: int` x 座標
        `y: int` y 座標
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = int(x)
        self.y = int(y)

#定義一個二維向量 繼承自Position2d
class Vector2d(Position2d):
    """
    二維向量

    args:
        `x: int` x 座標
        `y: int` y 座標
    """
    
    #向量的長度
    @property
    def size(self) -> int:
        pass

#二次加載 新增 dot, angle
@overload
class Vector2d:
    #向量的長度
    @property
    def size(self) -> int:
        """
            向量的長度
        """
        return math.sqrt(self.x**2+self.y**2)
    
    #取得與某向量的內積
    def dot(self, v: Vector2d) -> int:
        """
        取得與某向量的內積

        args:
            `v: Vector2d` 某向量
        """
        return self.x * v.x + self.y * v.y
    
    #取得與某向量的夾角
    def angle(self, v: Vector2d) -> int:
        """
        取得與某向量的夾角

        args:
            `v: Vector2d` 某向量
        """
        try:
            return math.degrees(math.acos(self.dot(v)/(self.size * v.size)))

        except:
            return 0
            
# 根據傳入的 21 個節點座標，得到該手指的角度
def hand_angle(hand_: list[Position2d]) -> list[int]:
    """
        根據傳入的 21 個節點座標，得到該手指的角度

        args:
            `hand_: list[Position2d]` 節點座標陣列
    """
    # 根據回傳的座標將其轉換為向量
    def matrix(a: int, b: int) -> Vector2d:
        return Vector2d(hand_[a].x-hand_[b].x, hand_[a].y - hand_[b].y)
    
    angle = []
    # 大拇指
    angle.append(matrix(0, 2).angle(matrix(3, 4)))

    # 食指
    angle.append(matrix(0, 6).angle(matrix(7, 8))) 

    # 中指
    angle.append(matrix(0, 10).angle(matrix(11, 12)))
    
    # 無名指
    angle.append(matrix(0, 14).angle(matrix(15, 16)))

    # 小拇指
    angle.append(matrix(0, 18).angle(matrix(19, 20)))

    return angle

# 根據 5 根手指角度判斷為何種手勢
def hand_pos(angle: list[int]):
    """
    根據 5 根手指角度判斷為何種手勢
    
    args:
        `angle: list[int]`
    """
    f1, f2, f3, f4, f5 = angle  

    if is_good(f1, f2, f3, f4, f5):
        return 'Good'
    
    elif is_middle(f1, f2, f3, f4, f5):
        return 'No'
    
    elif is_rock(f1, f2, f3, f4, f5):
        return 'ROCK!'
    
    elif is_zero(f1, f2, f3, f4, f5):
        return '0'
    
    elif is_one(f1, f2, f3, f4, f5):
        return '1'
    
    elif is_two(f1, f2, f3, f4, f5):
        return '2'
    
    elif is_ok(f2, f3, f4, f5):
        return 'Ok'

    elif is_three(f1, f2, f3, f4, f5):
        return '3'
    
    elif is_four(f1, f2, f3, f4, f5):
        return '4'
    
    elif is_five(f1, f2, f3, f4, f5):
        return '5'
    
    elif is_six(f1, f2, f3, f4, f5):
        return '6'
    
    elif is_seven(f1, f2, f3, f4, f5):
        return '7'
    
    elif is_eight(f1, f2, f3, f4, f5):
        return '8'
    
    elif is_nine(f1, f2, f3, f4, f5):
        return '9'
    
    else:
        return ' '

cap = cv2.VideoCapture(0)            # 讀取攝影機
fontFace = cv2.FONT_HERSHEY_SIMPLEX  # 字型
lineType = cv2.LINE_AA               # 邊框

mp_hands = hands #手部模型
port_4 = "http://192.168.4.1/4/"
port_0 = "http://192.168.4.1/0/"
port_2 = "http://192.168.4.1/2/"


def off(url):
    return get(url+"off")

def on(url):
    return get(url+"on")

def _default():
    off(port_4)
    off(port_2)
    off(port_0)
    return

# 啟用偵測手掌
with mp_hands.Hands(
    max_num_hands=1, #可偵測手勢的最大數量
    ) as hand:

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    w, h = 540, 310                                  # 影像尺寸
    while True:
        ret, img = cap.read()                        # 讀取圖像
        img = cv2.resize(img, (w, h))                # 縮小尺寸，加快處理效率

        if not ret:
            print("Cannot receive frame")
            break
        
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉換成 RGB 色彩
        results = hand.process(img2)                # 偵測手勢
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                finger_points = []                   # 記錄手指節點座標的串列
                for i in hand_landmarks.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    finger_points.append(Position2d(i.x*w, i.y*h))

                if finger_points:
                    finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                    text = hand_pos(finger_angle)            # 取得手勢所回傳的內容
                    cv2.putText(img, text, (30, 120), fontFace, 3, (107, 142, 35), 10, lineType) # 印出文字

                    if text == '0':
                        _default()

                    elif text == "1":
                        on(port_4)

                    elif text == "2":
                        on(port_0)

                    elif text == "3":
                        on(port_2)

                    

        cv2.imshow('手部感測系統', img)
        if cv2.waitKey(1)==ord("q"):
            break
        
cap.release()
cv2.destroyAllWindows()