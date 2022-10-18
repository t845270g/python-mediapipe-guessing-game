import cv2
import mediapipe as mp
import matplotlib.pyplot as plt
from math import sqrt 
hands檔案 = mp.solutions.hands
utils檔案= mp.solutions.drawing_utils
點的型式=utils檔案.DrawingSpec(color=(0,0,255),thickness=2,circle_radius=3)#實體化點的型式
線條型式=utils檔案.DrawingSpec(color=(0,255,0),thickness=5)#實體化線條型式，圓半徑設了也沒用，因為是線
def 判斷出拳(複製視窗, results):
    # 將手的每個手指的尖端座標的索引存儲在列表中。[8食指,12中指,16無名指,20小指]
    每個指尖的編號 = [hands檔案.HandLandmark.INDEX_FINGER_TIP, hands檔案.HandLandmark.MIDDLE_FINGER_TIP,
                        hands檔案.HandLandmark.RING_FINGER_TIP, hands檔案.HandLandmark.PINKY_TIP]
    
    # 初始化一個字典來存儲雙手每個手指的狀態（即，True 表示打開，False 表示關閉）。
    #[右手拇指,右手食指,右手中指,右手無名指,右手小指,   左手拇指,左手食指,左手中指,左手無名指,左手小指]
    剪刀_石頭_布 = {'剪刀': False , '石頭': False , '布': False,'Left':  False,'Right' : False}
    #for handLms in 手掌點座標:#針對所有座標點跑迴圈
                #utils檔案.draw_landmarks(複製視窗,handLms,hands檔案.HAND_CONNECTIONS,點的型式,線條型式)
    # 跑過所有[classification {index: 1  score: 0.9539452195167542  label: "Right"}]字典清單
    for hand_手指, hand_偵測左右手資訊 in enumerate(results.multi_handedness):
        #偵測到一隻手hand_手指=0  偵測到雙手會到hand_手指=1
        
        #存下偵測到的是左手還是右手。
        Right_or_Left = hand_偵測左右手資訊.classification[0].label
        #偵測到手的話會產生一個列表，列表內容如下[classification {index: 1  score: 0.9539452195167542  label: "Right"}]
        #取出第0個列表的label值，"Right" or "Left"
        
        #偵測到的手的座標。
        hand_座標們 =  results.multi_hand_landmarks[hand_手指]#所有座標存起來
                # 查詢大拇指尖與第三節的x座標
        小指_x = hand_座標們.landmark[20].x
        大拇指尖_x = hand_座標們.landmark[hands檔案.HandLandmark.THUMB_TIP].x
        大拇指座標=(hand_座標們.landmark[4].x*1280,hand_座標們.landmark[4].y*960)
        食指指尖座標=(hand_座標們.landmark[8].x*1280,hand_座標們.landmark[8].y*960)
        拇指指尖到食指指尖距離=int(sqrt((大拇指座標[0]-食指指尖座標[0])**2+(大拇指座標[1]-食指指尖座標[1])**2))
       

        #THUMB_TIP是4，4指的是大拇指尖，找出所有座標的第4筆資料的x座標，也就是大拇指尖x座標值回存
        大拇指第三節 = hand_座標們.landmark[hands檔案.HandLandmark.THUMB_TIP - 2].x
        #THUMB_TIP是4，4-2=2，2指的是大拇指第三節，找出所有座標的第2筆資料的x座標，也就是大拇指第三節x座標值回存
        四指指尖y座標=[]
        四指第三節y座標=[]
        # [8食指,12中指,16無名指,20小指] 
        # [hands檔案.HandLandmark.INDEX_FINGER_TIP, hands檔案.HandLandmark.MIDDLE_FINGER_TIP,hands檔案.HandLandmark.RING_FINGER_TIP, hands檔案.HandLandmark.PINKY_TIP]
        for tip_index in 每個指尖的編號:
            # hands檔案.HandLandmark.INDEX_FINGER_TIP的name為"INDEX_FINGER_TIP"，底線拆分成列表['INDEX', 'FINGER', 'TIP']，取得第0個值回存
            哪指的指尖_手指頭名字 = tip_index.name.split("_")[0]
            四指指尖y座標.append(hand_座標們.landmark[tip_index].y)
            四指第三節y座標.append(hand_座標們.landmark[tip_index - 2].y)
        
        if Right_or_Left=='Left':
            剪刀_石頭_布['Left'] = True  
        elif Right_or_Left=='Right':
            剪刀_石頭_布['Right'] = True  

        #通過比較尖端和點地標的 y 坐標來檢查手指是否向上。
        if 四指指尖y座標[0]<四指第三節y座標[0] and  四指指尖y座標[1]<四指第三節y座標[1] and 四指指尖y座標[2]>四指第三節y座標[2] and 四指指尖y座標[3]>四指第三節y座標[3]:
            if Right_or_Left=='Right' and 大拇指尖_x>大拇指第三節  or Right_or_Left=='Left' and 大拇指尖_x<大拇指第三節:
                剪刀_石頭_布['剪刀'] = True

        elif  四指指尖y座標[0]>四指第三節y座標[0] and  四指指尖y座標[1]>四指第三節y座標[1] and 四指指尖y座標[2]>四指第三節y座標[2] and 四指指尖y座標[3]>四指第三節y座標[3]:
            if Right_or_Left=='Right' and 大拇指尖_x>大拇指第三節  or Right_or_Left=='Left' and 大拇指尖_x<大拇指第三節:
                剪刀_石頭_布['石頭'] = True  


        elif 四指指尖y座標<四指第三節y座標 :
            if Right_or_Left=='Right' and 大拇指尖_x<大拇指第三節  or Right_or_Left=='Left' and 大拇指尖_x>大拇指第三節:
                剪刀_石頭_布['布'] = True
        
        #if 四指指尖y座標[1]<四指第三節y座標[1] and 四指指尖y座標[2]<四指第三節y座標[2] and 四指指尖y座標[3]<四指第三節y座標[3] and 四指指尖y座標[0]>四指第三節y座標[0] and 拇指指尖到食指指尖距離<50:
            #if Right_or_Left=='Right' and 大拇指尖_x<小指_x  or Right_or_Left=='Left' and 大拇指尖_x>小指_x:
                #剪刀_石頭_布_ok['ok'] = True

        return 剪刀_石頭_布
    else:
        # Return the output image, the status of each finger and the count of the fingers up of both hands.
        return 剪刀_石頭_布

