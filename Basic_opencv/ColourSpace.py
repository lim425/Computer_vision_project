import cv2
import os

img_path = os.path.join('.', 'bird.jpg')
img = cv2.imread(img_path)


img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

cv2.imshow("image", img)
cv2.imshow("image_hsv", img_hsv)
# cv2.imshow("image_grey", img_grey)
cv2.waitKey(0)


