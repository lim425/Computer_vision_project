import numpy as np
from ultralytics import YOLO
import cv2
import cvzone
import math
import time
from sort import *
#for video
cap = cv2.VideoCapture("../Videos/cars.mp4")


model = YOLO('../Yolo_Weight/yolov8l.pt')

classNames = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat", "traffic light", "fire hydrant",
              "stop sign", "parking meter", "bench", "bird", "cat", "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe",
              "backpack", "umbrella" , "handbag" , "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",  "kite", "baseball bat",
              "baseball glove", "skateboard","surfboard", "tennis racke","bottle", "wine glass", "cup", "fork", "knife","spoon", "bowl",
              "banana" ,"apple", "sandwich", "orange" ,"broccoli", "carrot" ,"hot dog" , "pizza" , "donut", "cake" , "chair", "couch", "potted plant",
              "bed", "dining table", "toilet", "tv", "laptop" , "mouse", "remote", "keyboard", "cell phone" ,"microwave" , "oven" ,"toaster" ,
              "sink" , "refrigerator" ,"book" , "clock", "vase" ,"scissors", "teddy bear", "hair drier", "toothbrush"]

prev_frame_time = 0
new_frame_time = 0

mask = cv2.imread("mask.png")

# Tracking
tracker = Sort(max_age=20, min_hits=3, iou_threshold=0.3)

limits = [400, 297, 673, 297]
totalCount = []

while True:
    new_frame_time = time.time()

    success, img = cap.read()
    imgRegion = cv2.bitwise_and(img, mask)
    imgGraphics = cv2.imread("graphics.png", cv2.IMREAD_UNCHANGED)
    img = cvzone.overlayPNG(img, imgGraphics, (0, 0))
    results = model(imgRegion, stream=True)

    detections = np.empty((0, 5))

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            w, h = x2 - x1, y2 - y1


            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100

            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if currentClass == "car" or currentClass == "truck" or currentClass == "bus"\
                or currentClass == "motorcycle" and conf > 0.3:
                # cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                # cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                #                    scale=0.6, thickness=1, offset=3)
                currentArray = np.array([x1,y1,x2,y2,conf])
                detections = np.vstack((detections, currentArray))

    resultsTracker = tracker.update(detections)
    cv2.line(img, (limits[0], limits[1]), (limits[2],limits[3]), (0,0,255), 5)
    for result in resultsTracker:
        x1, y1, x2, y2, id = result
        x1, y1, x2, y2, id = int(x1), int(y1), int(x2), int(y2), int(id)
        w, h = x2 - x1, y2 - y1
        cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=2, colorR=(255,0,255))
        cvzone.putTextRect(img, f'{int(id)}', (max(0, x1), max(35, y1)),
                           scale=2, thickness=3, offset=10)

        cx, cy = x1+w//2, y1+h//2
        cv2.circle(img, (cx,cy),5,(255,0,255), cv2.FILLED)

        if limits[0] < cx < limits[2] and limits[1] - 15 < cy < limits[1] + 15:
            if totalCount.count(id) == 0:
                totalCount.append(id)
                cv2.line(img, (limits[0], limits[1]), (limits[2], limits[3]), (0, 255, 0), 5)

    cv2.putText(img, str(len(totalCount)), (255, 100), cv2.FONT_HERSHEY_PLAIN, 5, (50, 50, 255), 8)

    cv2.imshow("Image", img)
    # cv2.imshow("ImageRegion", imgRegion)

    fps = 1 / (new_frame_time - prev_frame_time)
    prev_frame_time = new_frame_time
    print("fps:", fps)

    if cv2.waitKey(1) & 0xff == ord("q"):
        break
cv2.destroyAllWindows()
