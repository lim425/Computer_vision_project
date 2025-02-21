import cv2

# Ensure correct path formatting with raw strings
img = cv2.imread(r"Resources\Lambo.png")
classNames = []
classFile = r"ObjectDetector\coco.names"
with open(classFile, "rt") as f:
    classNames = f.read().rstrip("\n").split("\n")

configPath = r"ObjectDetector\ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
weightsPath = r"ObjectDetector\frozen_inference_graph.pb"

# Load model
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Perform detection
classIds, confs, bbox = net.detect(img, confThreshold=0.5)
print(classIds, bbox)

# Draw bounding boxes and labels on detected objects
for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
    cv2.rectangle(img, box, color=(0, 255, 0), thickness=2)
    cv2.putText(img, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

# Display output
cv2.imshow("Output", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
