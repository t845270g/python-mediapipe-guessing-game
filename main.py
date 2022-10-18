from pickle import FALSE
import cv2,pygame,os,judge,ww
import mediapipe as mp
import numpy 
import random as rd
from datetime import datetime
pygame.init()
pygame.mixer.init()#音效模組初始化
utils檔案= mp.solutions.drawing_utils
hands檔案 = mp.solutions.hands
實體化手類別=hands檔案.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8,min_tracking_confidence=0.3)
#player_mini__img=pygame.image.load(os.path.join("000.png")).convert()
#pygame.display.set_icon(player_mini__img)
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)#打開鏡頭
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)#像素拉高
#1280w*960h像素
cv2.namedWindow('rock-paper-scissors', cv2.WINDOW_NORMAL)#開新視窗，視窗大小可變，視窗縮放到1280*960都不會失真

#音效
剪刀=pygame.mixer.Sound(os.path.join("001.mp3"))
石頭=pygame.mixer.Sound(os.path.join("002.mp3"))
布=pygame.mixer.Sound(os.path.join("003.mp3"))
win=pygame.mixer.Sound(os.path.join("win.mp3"))
lose=pygame.mixer.Sound(os.path.join("lose.mp3"))
peace=pygame.mixer.Sound(os.path.join("peace.mp3"))
winnermusic=pygame.mixer.Sound(os.path.join("winner.mp3"))
losermusic=pygame.mixer.Sound(os.path.join("loser.mp3"))

播放音效=False

def 猜拳判斷(電腦拳字串,手指狀態真假):
    if 電腦拳字串=="石頭":
        if 手指狀態真假["石頭"]==True:
            return "peace"
        elif 手指狀態真假["剪刀"]==True:
            return "lose"
        elif 手指狀態真假["布"]==True:
            return "win"


    if 電腦拳字串=="剪刀":
        if 手指狀態真假["石頭"]==True:
            return "win"
        if 手指狀態真假["剪刀"]==True:
            return "peace"
        if 手指狀態真假["布"]==True:
            return "lose"

    if 電腦拳字串=="布":
        if 手指狀態真假["石頭"]==True:
            return "lose"
        elif 手指狀態真假["剪刀"]==True:
            return "win"
        elif 手指狀態真假["布"]==True:
            return "peace"

def 電腦的字串():
    拳清單=["剪刀","石頭","布"]
    電腦出拳=rd.choice(拳清單)
    return 電腦出拳

def 顯示電腦的拳圖片(顯示電腦出拳的視窗,電腦出拳,x,y):
    if 電腦出拳=="石頭":
        ww.覆寫手指圖到視窗中(顯示電腦出拳的視窗,剪刀石頭布圖片路徑[1],x,y)
    if 電腦出拳=="剪刀":
        ww.覆寫手指圖到視窗中(顯示電腦出拳的視窗,剪刀石頭布圖片路徑[0],x,y)
    if 電腦出拳=="布":
        ww.覆寫手指圖到視窗中(顯示電腦出拳的視窗,剪刀石頭布圖片路徑[2],x,y) 

def 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場):
    if 輸贏=="win":
        if 玩家勝場>=贏幾場:
            cv2.putText(顯示用視窗,"WINNER!",(380,230),cv2.QT_FONT_NORMAL,4,(0,255,0),6)
            return "WINNER!"
        if 玩家敗場>=贏幾場:    
            cv2.putText(顯示用視窗,"LOSER!",(430,230),cv2.QT_FONT_NORMAL,4,(0,0,255),6)
            return "LOSER!" 
    if 輸贏=="lose":
        if 玩家勝場>=贏幾場:
            cv2.putText(顯示用視窗,"LOSER!",(430,230),cv2.QT_FONT_NORMAL,4,(0,0,255),6) 
            return "LOSER!"
        if 玩家敗場>=贏幾場:    
            cv2.putText(顯示用視窗,"WINNER!",(380,230),cv2.QT_FONT_NORMAL,4,(0,255,0),6)
            return "WINNER!" 

偵測到手=False
計算場次=True
初始化=False
第幾場=0
玩家勝場=0
玩家敗場=0
winner=0
loser=0
贏幾場=rd.randrange(1,6)
輸贏清單=["win","lose"]
輸贏=rd.choice(輸贏清單)
剪刀石頭布圖片路徑 = ["01.png","02.png","03.png"]
紀錄=[]


while True:#static_cast

    布林值, frame = cap.read()#存下鏡頭資料
    if 布林值:
        frame = cv2.flip(frame, 1)#鏡射影像
        顯示用視窗 = frame.copy()#複製影像
        frame.flags.writeable = False#不可讀寫，增加效能
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)#轉RGB
        results = 實體化手類別.process(imgRGB)#實體化物件
        frame.flags.writeable = True#轉回可讀寫才能修改視窗
        手掌點座標=results.multi_hand_landmarks#偵測到手會回傳座標
        
        if bool(手掌點座標)==True :#有手
            紀錄.append(pygame.time.get_ticks())#紀錄偵測到手的時候的時間列表
            偵測到手=True#控制倒數到猜拳判斷並呈現結果的開關，防止還沒從頭到尾執行一遍就又重新倒數了
            if 偵測到手==True:
                if (pygame.time.get_ticks() - 紀錄[0])<1000:
                    電腦出拳=電腦的字串()#在這段時間內會一直隨機選取一個電腦出拳，同時也將這段時間預留來緩衝一秒鐘
                    
                elif 1000<=(pygame.time.get_ticks() - 紀錄[0])<2000:
                    cv2.putText(顯示用視窗,"2",(570,430),cv2.QT_FONT_NORMAL,8,(0,250,250),8)#這段時間中顯示數字2
                    if 播放音效==False:#防止音效回音，用開關控制音效只播一次
                        剪刀.play()
                        播放音效=True
                elif 2000<=(pygame.time.get_ticks() - 紀錄[0])<3000:
                    cv2.putText(顯示用視窗,"1",(570,430),cv2.QT_FONT_NORMAL,8,(0,250,250),8)
                    if 播放音效==True:#防止音效回音，用開關控制音效只播一次
                        石頭.play()
                        播放音效=False
                elif 3000<=(pygame.time.get_ticks() - 紀錄[0])<3600:#0.6秒鐘內為出拳的時間
                    手勢判斷字典 = judge.判斷出拳(顯示用視窗, results)  
                    我的拳=手勢判斷字典#這段時間內可以產生不同拳，但是時間到會記錄最後出拳的結果，給人出拳緩衝作用
                    if 播放音效==False:#防止音效回音，用開關控制音效只播一次
                        布.play()
                        播放音效=True
                        
                elif 3600<=(pygame.time.get_ticks() - 紀錄[0])<4600: #拿到前一段時間記錄的最後出拳結果來判斷與電腦出拳結果來判斷
                    if 我的拳["石頭"]==True or 我的拳["剪刀"]==True  or 我的拳["布"]==True : 
                        if 計算場次==True:
                            if 猜拳判斷(電腦出拳,我的拳)=="lose":
                                玩家敗場+=1    
                                第幾場+=1
                                lose.play()
                                計算場次=False#用此開關來控制勝敗場次只會加一次就關閉，如果不這樣寫，出一次拳就會加到10去
                                播放音效=False
                            elif 猜拳判斷(電腦出拳,我的拳)=="win":
                                玩家勝場+=1 
                                第幾場+=1
                                win.play()
                                計算場次=False#用此開關來控制勝敗場次只會加一次就關閉，如果不這樣寫，出一次拳就會加到10去
                                播放音效=False
                            elif 猜拳判斷(電腦出拳,我的拳)=="peace":
                                第幾場+=1
                                peace.play()
                                計算場次=False#用此開關來控制勝敗場次只會加一次就關閉，如果不這樣寫，出一次拳就會加到10去
                                播放音效=False

                        if 我的拳['Right']==True:
                            if 猜拳判斷(電腦出拳,我的拳)=="win":
                                顯示電腦的拳圖片(顯示用視窗,電腦出拳,200,150) 
                                cv2.putText(顯示用視窗,"win",(480,420),cv2.QT_FONT_NORMAL,5,(0,250,0),5) 
                                if 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="WINNER!":
                                    初始化=True
                                elif 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="LOSER!":
                                    初始化=True

                            elif 猜拳判斷(電腦出拳,我的拳)=="lose":
                                顯示電腦的拳圖片(顯示用視窗,電腦出拳,200,150) 
                                cv2.putText(顯示用視窗,"lose",(480,420),cv2.QT_FONT_NORMAL,5,(0,0,250),5)
                                if 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="WINNER!":
                                    初始化=True
                                elif 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="LOSER!":
                                    初始化=True

                            elif 猜拳判斷(電腦出拳,我的拳)=="peace":   
                                cv2.putText(顯示用視窗,"peace",(400,420),cv2.QT_FONT_NORMAL,5,(0,250,250),5)
                                顯示電腦的拳圖片(顯示用視窗,電腦出拳,200,100)  

                        elif 我的拳['Left']==True:   
                            顯示電腦的拳圖片(顯示用視窗,電腦出拳,200,900)      
                            if 猜拳判斷(電腦出拳,我的拳)=="win":
                                cv2.putText(顯示用視窗,"win",(490,420),cv2.QT_FONT_NORMAL,5,(0,250,0),5)  
                                if 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="WINNER!":
                                    
                                    初始化=True
                                elif 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="LOSER!":
                                    
                                    初始化=True

                            elif 猜拳判斷(電腦出拳,我的拳)=="lose":
                                cv2.putText(顯示用視窗,"lose",(490,420),cv2.QT_FONT_NORMAL,5,(0,0,250),5)
                                if 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="WINNER!":
                                    初始化=True
                                elif 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="LOSER!":
                                    初始化=True
                     
                            elif 猜拳判斷(電腦出拳,我的拳)=="peace":
                                cv2.putText(顯示用視窗,"peace",(400,420),cv2.QT_FONT_NORMAL,5,(0,250,250),5)
                    else:
                        cv2.putText(顯示用視窗,"Shoot,please.",(300,400),cv2.QT_FONT_NORMAL,3,(0,250,250),5)
                        播放音效=False

                elif 4600<=(pygame.time.get_ticks() - 紀錄[0]):     
                    
                    if 初始化==True:
                        if 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="WINNER!":
                            winner+=1
                            winnermusic.play()
                            pygame.time.wait(1900) 
                        elif 輸贏家(輸贏,贏幾場,玩家勝場,玩家敗場)=="LOSER!":
                            losermusic.play()  
                            pygame.time.wait(1900) 

                            loser+=1
                        玩家勝場=0
                        玩家敗場=0
                        輸贏=rd.choice(輸贏清單)
                        贏幾場=rd.randrange(1,6)
                        初始化=False
                    紀錄=[]
                    偵測到手=False
                    計算場次=True  


        else:#無手
            cv2.putText(顯示用視窗,f"Are you ready?",(280,400),cv2.QT_FONT_NORMAL,3,(0,250,250),5)
            紀錄=[pygame.time.get_ticks()]
            播放音效=False

      
            
        cv2.putText(顯示用視窗,"you need",(250,50),cv2.QT_FONT_NORMAL,2,(255,250,255),2)
        if 輸贏=="win":
            cv2.putText(顯示用視窗,f"{輸贏} {贏幾場}",(590,50),cv2.QT_FONT_NORMAL,2,(0,255,0),5)
        else:
            cv2.putText(顯示用視窗,f"{輸贏} {贏幾場}",(590,50),cv2.QT_FONT_NORMAL,2,(0,0,255),5)
        cv2.putText(顯示用視窗,"rounds",(800,50),cv2.QT_FONT_NORMAL,2,(255,250,255),2)

        cv2.putText(顯示用視窗,"( shoot in 0.6 second )",(450,100),cv2.QT_FONT_NORMAL,1,(255,255,255),2)

        cv2.putText(顯示用視窗,"WINNER:"+f"{winner}",(10,30),cv2.QT_FONT_NORMAL,1,(0,250,0),2)
        cv2.putText(顯示用視窗,"LOSER:"+ f"{loser}",(10,60),cv2.QT_FONT_NORMAL,1,(0,0,255),2)

        cv2.putText(顯示用視窗,"LOSE:"+ f"{玩家敗場}",(250,650),cv2.QT_FONT_NORMAL,3,(0,0,255),5)
        cv2.putText(顯示用視窗,"WIN:"+f"{玩家勝場}",(730,650),cv2.QT_FONT_NORMAL,3,(0,250,0),5)



        cv2.putText(顯示用視窗,"no."+f"{第幾場}",(1150,700),cv2.QT_FONT_NORMAL,1,(255,255,255),1)   

        cv2.imshow('rock-paper-scissors', 顯示用視窗)

        k=cv2.waitKey(1)#https://www.wandouip.com/t5i114648/
        if cv2.getWindowProperty('rock-paper-scissors', cv2.WND_PROP_VISIBLE) <1:
            break
        if cv2.waitKey(1)==27:
            break 
    else:
        break
    #auto-py-to-exe 


cap.release()
cv2.destroyAllWindows()


#–icon=图标路径

#-F 打包成一个exe文件

#-w 使用窗口，无控制台

#-c 使用控制台，无窗口

#-p 指定exe依赖的包、模块

#-d 编译为debug模式，获取运行中的日志信息

#-D 创建一个目录，里面包含exe以及其他一些依赖性文件

#-clean 清理编译时临时文件

#-distpath 指定生成的exe存放目录

#-workpath 指定变异种临时文件存放的目录

#-version-file 添加exe版本信息

#pyinstaller -h 来查看参数

#1.pyinstaller -w -F --icon=a.ico main.py 指令轉檔，會產生__pycache__\build\dist\main.spec檔案
#__pycache__\build檔案不需要  是轉檔時產生的
#opencv轉檔會出現編碼問題需要在main.spec檔案加工
#https://stackoverflow.com/questions/67887088/issues-compiling-mediapipe-with-pyinstaller-on-macos

"""
加工步驟1.在main.spec檔案
block_cipher = None 後加入

def get_mediapipe_path():
    import mediapipe
    mediapipe_path = mediapipe.__path__[0]
    return mediapipe_path

2.pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)後加入

mediapipe_tree = Tree(get_mediapipe_path(), prefix='mediapipe', excludes=["*.pyc"])
a.datas += mediapipe_tree
a.binaries = filter(lambda x: 'mediapipe' not in x[0], a.binaries)

添加後，主程式終端機輸入pyinstaller --debug=all main.spec --windowed --onefile  除錯更新

"""