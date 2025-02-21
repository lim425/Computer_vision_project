import cv2
import numpy as np

print("Package Imported")

# image
img = cv2.imread("../Resources/Lena.png")
# cv2.imshow("image", img)

# gray
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# cv2.imshow("img_gray", img_gray)

# blur
k_size = 7
img_blur = cv2.GaussianBlur(img_gray, (k_size, k_size), 10)
# cv2.imshow("img_blur", img_blur)

# canny
kernel = np.ones((3, 3), dtype=np.int8)

img_edge = cv2.Canny(img, 100, 200)
img_edge_d = cv2.dilate(img, kernel, iterations=1) # increase the thickness
img_edge_e = cv2.erode(img, kernel, iterations=1) # decrease the thickness
cv2.imshow("img_edge", img_edge)
cv2.imshow("img_dilate", img_edge_d)
cv2.imshow("img_erode", img_edge_e)

cv2.waitKey(0)