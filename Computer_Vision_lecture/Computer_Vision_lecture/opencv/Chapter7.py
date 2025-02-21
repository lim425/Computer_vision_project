import cv2
import numpy as np

# Now you can import the file
import img_comb as imgCombine

path = ("../Resources/Cards.jpg")
img = cv2.imread(path)


def empty(a ):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)

cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 179, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 0, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

while True:
    img = cv2.imread(path)
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) #Heat, saturation, value

    hue_min_val = cv2.getTrackbarPos("Hue Min", "TrackBars")
    hue_max_val = cv2.getTrackbarPos("Hue Max", "TrackBars")
    sat_min_val = cv2.getTrackbarPos("Sat Min", "TrackBars")
    sat_max_val = cv2.getTrackbarPos("Sat Max", "TrackBars")
    val_min_val = cv2.getTrackbarPos("Val Min", "TrackBars")
    val_max_val = cv2.getTrackbarPos("Val Max", "TrackBars")
    
    print(hue_min_val, hue_max_val, sat_min_val, sat_max_val, val_min_val, val_max_val)

    lower = np.array([hue_min_val, sat_min_val, val_min_val])
    upper = np.array([hue_max_val, sat_max_val, val_max_val])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(img,img,mask=mask)


    # cv2.imshow("Original",img)
    # cv2.imshow("HSV",imgHSV)
    # cv2.imshow("Mask", mask)
    # cv2.imshow("Result", imgResult)

    imgStack = imgCombine.stackImages(0.6,([img,imgHSV],[mask,imgResult]))
    cv2.imshow("Stacked Images", imgStack)

    cv2.waitKey(1)