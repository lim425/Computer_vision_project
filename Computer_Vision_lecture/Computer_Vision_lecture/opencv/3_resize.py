import cv2
print("Package Imported")

# image
img = cv2.imread("../Resources/antam.png")
print(img.shape)

img_resize = cv2.resize(img, (640, 480))

cv2.imshow("images", img)
cv2.imshow("image_resize", img_resize)

y1, y2, x1, x2 = 50, 360, 200, 280
img_cropped = img_resize[y1:y2, x1:x2]
cv2.imshow("img_cropped", img_cropped)
cv2.waitKey(0)