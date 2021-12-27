import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import numpy as np
import glob

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)

detector = htm.handDetector()
files=[]
path = glob.glob("rasengan/*.png")
for img in path:
    n = cv2.imread(img,1)
    files.append(n)
rasengan=[]
size_ratio=3
for resizer in files:
    xshape=round(resizer.shape[1]/size_ratio)
    yshape=round(resizer.shape[0]/size_ratio)
    resizer=cv2.resize(resizer,(xshape,yshape))
    rasengan.append(resizer)


rasengan_count=0

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False )
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        cxa=round( (lmList[0][1]+lmList[9][1])/2 )
        cya=round( (lmList[0][2]+lmList[9][2])/2 )
        cxb=round( (lmList[0][1]+lmList[13][1])/2 )
        cyb=round( (lmList[0][2]+lmList[13][2])/2 )
        cx=round ((cxa+cxb/2))
        cy=round ((cya+cyb/2))
        img2=rasengan[rasengan_count]

        for i in range (0,img2.shape[0]):
            for j in range (0,img2.shape[1]):
                if(img2[i][j][0]>150):
                    img[i+cya-round(img2.shape[0]/2)][j+cxa-round(img2.shape[1]/2)]=img2[i][j]

        rasengan_count += 1

    if(rasengan_count==(len(rasengan))):
        rasengan_count=0


    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.imshow("Image", img)
    cv2.waitKey(1)