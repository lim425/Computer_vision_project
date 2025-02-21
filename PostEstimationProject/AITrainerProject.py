import cv2
import mediapipe as mp
import time

import numpy as np

import PoseEstimationModule as pm


cap = cv2.VideoCapture("PoseVideo/PoseVideo1.mp4")
# cap = cv2.VideoCapture(0)
pTime = 0

detector = pm.poseDetector()

count = 0
dir = 0

while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)

    if len(lmList) != 0:
        # # Left arm
        # detector.findAngle(img, 11, 13, 15)

        # Right arm
        angle = detector.findAngle(img, 12, 14, 16)
        # arm angle in the video is between 185 ~ 335
        percentage = np.interp(angle, (185, 335), (0, 100))
        # print(angle, percentage)

        # Check for the dumbbell curls
        if percentage == 100 and dir == 0:
            count += 0.5
            dir = 1
        if percentage == 0 and dir == 1:
            count += 0.5
            dir = 0
        print(count)

        cv2.rectangle(img, (0, 550), (100, 640), (0, 255, 0), -1)
        cv2.putText(img, f'{str(int(count))}', (30, 620), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)




    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                (255, 0, 0), 3)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()