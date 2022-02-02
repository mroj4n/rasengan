# Rasengan filter
#### _An AI&CV project_

This program uses Artificial intelligence and computer vision to place a Rasengan on the palm of a user’s hand. 
This program also includes a volume slider that can change the system volume of a PC using your index finger. 


## Dependancies 
##### - mediapipe
--```pip install mediapipe``` 
##### - cv2
-- ```pip install opencv-python```
##### - numpy
-- ```pip install numpy``` 
##### - glob
--```pip install glob2```
##### - pycaw
-- ```pip install pycaw``` (windows only)

## Program description
#### Detecting hands
This program uses mediapipe which is an opensource AI algorithm to detect hands by google. 
It uses the HandTrackingModule.py to do the detection of the hand. This Module is reusable for other applications too as  all it does is return the landmarks on a hand. 
#### Rasengan
The program places a Rasengan on palm of the user. It does this in real-time video. The Rasengan that is placed is animated. This is done by using different frames of the Rasengan and then changing each frame of Rasengan based on the change of frame of the actual output.
#### Volume Slider
This code also supports controlling system volume using a slider. This was mostly done to test out the hand detection and the code was left in as a proof of concept. 
To toggle the slider please check line 14 in main.py



## How to run
- Clone the repo
- Install all the required dependancies
- Run ```python main.py```



## Closing remarks
- This project was done for Artificial Intelligence and Computer Vision project for Politechnika Wrocławska
