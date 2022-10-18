import cv2
def 覆寫手指圖到視窗中(視窗,圖片路徑,x,y):
    視窗高, 視窗寬, _ = 視窗.shape#圖片的寬高
    ori = cv2.imread(f'{圖片路徑}', cv2.IMREAD_UNCHANGED)
    ori=cv2.resize(ori,(300,300),fx=1,fy=1)
    ori_alpha=ori[:,:,-1]
    ori_BGR=ori[:,:,:-1]
    視窗_range = 視窗[x : x+300 ,   y   :  y+300  ]
    視窗_range[ori_alpha==255] = ori_BGR[ori_alpha==255]
    視窗[x : x+300 ,   y   :  y+300  ]=視窗_range
