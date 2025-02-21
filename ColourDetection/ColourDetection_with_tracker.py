import numpy as np
import cv2
from PIL import Image
from tracker import create_trackbars, get_trackbar_values

# Set up the webcam
width, height = 640, 360
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
cam.set(cv2.CAP_PROP_FPS, 30)
cam.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# Create Tracker
create_trackbars("my tracker")
cv2.moveWindow("my tracker", width, 0)

while True:
    # Capture frame
    ignore, frame = cam.read()
    frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Get trackbar values
    hueLow, hueHigh, satLow, satHigh, valLow, valHigh = get_trackbar_values()

    # Create a desired lower limit and upper limit
    lowerBound = np.array([hueLow, satLow, valLow])
    upperBound = np.array([hueHigh, satHigh, valHigh])

    # Create a mask
    myMask = cv2.inRange(frameHSV, lowerBound, upperBound)
    myMaskSmall = cv2.resize(myMask, (int(width / 2), int(height / 2)))  # resize the window
    cv2.imshow("my mask", myMaskSmall)
    cv2.moveWindow("my mask", 0, height + 150)

    # Create the bounding box for the object
    myMask_ = Image.fromarray(myMask)
    bbox = myMask_.getbbox()
    if bbox is not None:
        x1, y1, x2, y2 = bbox
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 5)

    # Show the main frame
    cv2.imshow("myWebcam", frame)
    cv2.moveWindow("myWebcam", 0, 0)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xff == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()
