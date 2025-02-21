import cv2

print(cv2.__version__)

width = 640
height = 360

# make the video more smooth, reduce the video setup time
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

while True:
    ignore, img = cam.read()

    cv2.imshow("myWebcam", img)
    # cv2.moveWindow("myWebcam", 0, 0)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cam.release()
cv2.destroyAllWindows()