import cv2
import mediapipe as mp
import time

width = 640
height = 360
# make the video more smooth, reduce the video setup time
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

cTime = 0
pTime = 0

while True:
    ignore, img = cam.read()

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)

    cv2.imshow("myWebcam", img)
    cv2.moveWindow("myWebcam", 0, 0)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()
