import cv2
print("Package Imported")

# image
# img = cv2.imread("../Resources/antam.png")
img = cv2.imread("C:/Users/Asus/PycharmProjects/ComputerVisionProject/Computer_Vision_lecture/Computer_Vision_lecture/Resources/antam.png")

cv2.imshow("images", img)
cv2.waitKey(0)

# video
# cap = cv2.VideoCapture("../Resources/video_sample_1.mp4")
# while True:
#     success, img = cap.read()
#     cv2.imshow("video output", img)
#     if cv2.waitKey(1) & 0xff == ord("q"):
#         break
# cv2.destroyAllWindows()

# webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 640) #3-width
# cap.set(4, 480) #4-high
# cap.set(10, 100) #10-brightness
#
# while True:
#     success, img = cap.read()
#     cv2.imshow("video output", img)
#     if cv2.waitKey(1) & 0xff == ord("q"):
#         break
# cv2.destroyAllWindows()