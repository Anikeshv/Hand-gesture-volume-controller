import cv2
import mediapipe as mp
import time
import numpy as np
import pycaw
import Handdetector_module as htm

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities
from pycaw.pycaw import IAudioEndpointVolume

# detector = htm.Handdetector

def main():
    cTime , pTime = 0 , 0
    cap = cv2.VideoCapture(0)
    detector = htm.Handdetector(detectionCon = 0.7)

    device = AudioUtilities.GetSpeakers()
    interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))

    print(f"Volume range: {volume.GetVolumeRange()[0]} dB - {volume.GetVolumeRange()[1]} dB")
    Min_vol = volume.GetVolumeRange()[0]
    Max_vol = volume.GetVolumeRange()[1]
    vol=0
    Bar_vol=400
    Per_vol=0

    # Check if camera opened successfully
    if not cap.isOpened():
       print("Error: Could not open camera.")

    else:
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    while True:
        # Capture frame-by-frame   
        ret, img = cap.read()
        if not ret:
            print("Can't receive frame. Exiting...")
            break

        img = detector.Findhands(img)
        lmList = detector.Findposition(img , draw =False)
        if len(lmList)!= 0 :
            # print(lmList)
            # print(lmList[4] ,lmList[8])

            x1 ,y1 = lmList[4][1] ,lmList[4][2]
            x2 ,y2 = lmList[8][1] ,lmList[8][2]
            cv2.circle(img, (x1,y1), 10, (255,0,255), cv2.FILLED)
            cv2.circle(img, (x2,y2), 10, (255,0,255), cv2.FILLED)
            cv2.line(img, (x1,y1), (x2,y2), (225,0,225), 3)

            cx , cy = (x1+x2)//2 , (y1+y2)//2
            cv2.circle(img, (cx,cy), 7, (255,0,255), cv2.FILLED)

            Length = ((x2-x1)**2 +(y2-y1)**2)**(1/2)
            # print(Length)
            if Length<35 :
                cv2.circle(img, (cx,cy), 7, (0,225,0), cv2.FILLED)

            # Handrange 35 - 150
            #  Vol range -65 - 0
            vol = np.interp(Length,[20,150],[Min_vol,Max_vol])
            Bar_vol = np.interp(Length,[20,150],[400,130])
            Per_vol = np.interp(Length,[20,150],[0,100])
            # print(vol)
            volume.SetMasterVolumeLevel(vol, None)

        cv2.rectangle(img ,(30,130),(80,400),(0,255,0),3)
        cv2.rectangle(img ,(30,int(Bar_vol)),(80,400),(0,255,0),cv2.FILLED)
        cv2.putText(img , f'{int(Per_vol)} %', (40,450) , cv2.FONT_HERSHEY_COMPLEX , 1 , (225,0,0) , 3)


        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img , f'FPS: {(int(fps))}', (10,70) , cv2.FONT_HERSHEY_COMPLEX , 1 , (225,0,0) , 3)

        # Display the resulting frame
        cv2.imshow('Video Frame', img)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()



if __name__ == "__main__":
    main()

 
















