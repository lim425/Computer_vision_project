import cv2

cap = cv2.VideoCapture("test2.mp4")
while True:
    success, img = cap.read()
    cv2.imshow("video output", img)
    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()