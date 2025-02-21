import cv2
import numpy as np

# img = np.zeros((500, 500, 3), np.uint8)
img = cv2.imread("../Resources/Lena.png")
print(img.shape)
# line
# cv2.line(img, (0, 0), (200, 200), (255, 0, 0), 2)

# rectangle
cv2.rectangle(img, (200, 200), (400, 400), (0, 255, 0), 2)


# circle
# cv2.circle(img, (256, 150), 100, (0, 0, 255), 1)

# text
cv2.putText(img, "I'm Lena", (210, 200), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)

cv2.imshow("img", img)
cv2.waitKey(0)

