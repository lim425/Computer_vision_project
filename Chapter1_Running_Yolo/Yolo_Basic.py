from ultralytics import YOLO
import cv2

model = YOLO('../Yolo_Weight/yolov8m.pt')

results = model("image1.jpg", show=True)

cv2.waitKey(0)