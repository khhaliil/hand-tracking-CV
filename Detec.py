import cv2
import time
import os
import HandTrackModule as htm
import numpy as np

wCam, hCam = 640*1.5, 480*1.5


cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "data"
myList = os.listdir(folderPath)
print(myList)
overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
    # print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0

detector = htm.handDetector(detectionCon=0)

tipIds = [4, 8, 12, 16, 20]


def func(pos):
    print(pos)


circles = np.zeros((2, 2), np.int_)
counter = 0


def MouseClick(event, x, y, flags, parms):
    global counter
    if counter >= 2:
        counter = 0
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        circles[counter] = x, y
        print(circles)
        counter += 1


cv2.namedWindow("pos")
cv2.createTrackbar('height', "pos", 40, 200, func)
cv2.createTrackbar('width', "pos", 90, 200, func)

# Define bounding box
box_top = 10
box_bottom = 300
box_left = 10
box_right = 300

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=True)

    # Draw bounding box
    cv2.rectangle(img, (circles[0][0], circles[0][1]),
                  (circles[1][0], circles[1][1]), (255, 0, 0), 2)

    if len(lmList) != 0:
        fingers = []

        # Check if the hand is within the bounding box
        if circles[0][0] < lmList[0][1] < circles[1][0] and circles[0][1] < lmList[0][2] < circles[1][1]:

            # Thumb
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # 4 Fingers
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            totalFingers = fingers.count(1)
            print(totalFingers)

            cv2.putText(img, str(--totalFingers), (cv2.getTrackbarPos("height", "pos"), cv2.getTrackbarPos("width", "pos")), cv2.FONT_HERSHEY_PLAIN,
                        8, (0, 255, 0), 25)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN,
                3, (255, 0, 0), 3)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", MouseClick)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break
