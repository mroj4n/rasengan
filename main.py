import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import numpy as np
import glob
import os

isWindows = False
if os.name == 'nt':
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    isWindows = True  # change this variable to false if you want volume slider to be turned off. It is turned on for windows by default


devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)

detector = htm.handDetector()
files = []
path = glob.glob("rasengan/*.png")
for img in path:
    n = cv2.imread(img, 1)
    files.append(n)
rasengan = []
size_ratio = 3
for resizer in files:
    xshape = round(resizer.shape[1]/size_ratio)
    yshape = round(resizer.shape[0]/size_ratio)
    resizer = cv2.resize(resizer, (xshape, yshape))
    rasengan.append(resizer)


rasengan_count = 0
current_vol_height = 39

while True:
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    height, width, channels = img.shape

    if isWindows:
        cv2.rectangle(img, (height-1, 39), (height+41,
                                            height-39), (255, 255, 255), 3)

    if len(lmList) != 0:
        cxa = round((lmList[0][1]+lmList[9][1])/2)
        cya = round((lmList[0][2]+lmList[9][2])/2)

        # to resize the image depending of the distance between tip of middle to palm
        rasengan_to_hand_ratio = rasengan[rasengan_count].shape[1] / \
            (lmList[0][2]-lmList[12][2])
        rasengan_size_x = abs(
            round(1.5 * (rasengan[rasengan_count].shape[1]/rasengan_to_hand_ratio)))
        rasengan_size_y = abs(
            round(1.5 * (rasengan[rasengan_count].shape[0]/rasengan_to_hand_ratio)))
        img2 = cv2.resize(rasengan[rasengan_count],
                          (rasengan_size_x, rasengan_size_y))

        horizontal_offset = round((lmList[0][1]+lmList[5][1])/2)-round(
            (lmList[0][1]+lmList[13][1])/2)  # For tilting of hand

        for i in range(0, img2.shape[0]):
            for j in range(0, img2.shape[1]):
                if(img2[i][j][0] > 150):
                    img[i+cya-round(img2.shape[0]/2)][j+cxa -
                                                      round(img2.shape[1]/2)-horizontal_offset] = img2[i][j]

        rasengan_count += 1

        if isWindows and lmList[8][1] > height-1 and lmList[8][1] < height+41 and lmList[8][2] > 39:
            current_vol_height = lmList[8][2]
            vol_percentage = 100 - ((lmList[8][2] / height)*100)
            volume.SetMasterVolumeLevelScalar(
                (round(vol_percentage)/100), None)

    if isWindows:
        cv2.rectangle(img, (height, current_vol_height),
                      (height+40, height-40), (0, 0, 0), -1)

    if(rasengan_count == (len(rasengan))):
        rasengan_count = 0

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.imshow("Image", img)
    cv2.waitKey(1)
