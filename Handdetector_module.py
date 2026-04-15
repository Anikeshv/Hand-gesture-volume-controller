import cv2
import mediapipe as mp
import time

class Handdetector():

    def __init__(self, mode=False , maxHands= 2, detectionCon = 0.5, trackCon = 0.5):
        
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.maxHands,
            min_detection_confidence=self.detectionCon,
            min_tracking_confidence=self.trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils

    def Findhands(self, img , Draw=True):

        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                    if Draw:
                        self.mpDraw.draw_landmarks(img, handLms , self.mpHands.HAND_CONNECTIONS)
        return img
    
    def Findposition(self ,img ,HandNo=0 ,draw=True):

        lmList=[]
        if self.results.multi_hand_landmarks:
            MyHand = self.results.multi_hand_landmarks[HandNo]

            
            for id , lm in enumerate(MyHand.landmark):
                h , w, c = img.shape
                cx , cy = int (lm.x*w) , int (lm.y*h)
                lmList.append([id, cx, cy])
                # lmList=[id, cx, cy]
                if draw :
                    cv2.circle(img , (cx,cy) ,7, (225,0,225), cv2.FILLED)
        return lmList

def main():
    cTime , pTime = 0 , 0
    cap = cv2.VideoCapture(0)
    detector = Handdetector()

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
        lmList = detector.Findposition(img)
        if len(lmList)!=0 :
            print(lmList)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img , str(int(fps)), (10,70) , cv2.FONT_HERSHEY_COMPLEX , 2 , (225,0,225) , 3)

        # Display the resulting frame
        cv2.imshow('Video Frame', img)
        
        # Press 'q' to exit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()



if __name__ == "__main__":
    main()