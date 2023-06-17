import os
import cv2
import time
import HandTrackModule as htm
#########################################
cameraNum = 0
DataFolderPath = "data"

########################################
cap = cv2.VideoCapture(cameraNum)
List = os.listdir(DataFolderPath)
#print(List)

overlayList = []
for imgPath in List:
    image=cv2.imread(f'{DataFolderPath}/{imgPath}')
    overlayList.append(image)    
#print(len(overlayList))
ptime = 0 

detector = htm.handDetector(detectionCon=0.7)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    imList = detector.findPosition(img,draw=True)

    h,w,c = overlayList[1].shape 
    img[0:h,0:w] = overlayList[1]

    ctime=time.time()
    fps=1/(ctime-ptime)
    ptime=ctime
    height,width,chan=img.shape
    cv2.putText(img,f'FPS: {int(fps)}',(height-80,70),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),2)

    cv2.imshow("org", img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
