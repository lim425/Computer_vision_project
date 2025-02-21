from ultralytics import YOLO
import cv2
import cvzone
import pyttsx3
import threading

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

model = YOLO("C:/Users/Asus/PycharmProjects/ComputerVisionProject/Robocup_assignment/best_v4_jy.pt")

classNames = ['cup', 'shoes']

color = (255, 0, 255)
text = "NONE"

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

while True:
    ret, img_ori = cap.read()
    img = cv2.flip(img_ori, 1)

    frame_height = img.shape[0]

    has_cup = False
    has_shoes = False

    results = model(img, stream=True)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            w, h = x2 - x1, y2 - y1
            # Confidence level
            conf = round(box.conf[0].item(), 2)
            # Class name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if conf > 0.40:
                cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                                   scale=1.0, thickness=1, offset=3)
                if currentClass == "cup":
                    has_cup = True
                elif currentClass == "shoes":
                    has_shoes = True

    if has_cup and not has_shoes:
        text = "Welcome!"
        color = (0, 255, 0)
    elif has_cup and has_shoes:
        text = "Please take off ur shoes!"
        color = (0, 255, 255)
    elif not has_cup and not has_shoes:
        text = "Please bring ur drink"
        color = (255, 0, 0)
    else:
        text = "Take off ur shoes and bring ur drink"
        color = (0, 0, 255)

    cvzone.putTextRect(img, text, (0, 50), scale=1.7, thickness=1, colorR=color, colorT=(0, 0, 0))
    cvzone.putTextRect(img, f'Has shoes: {has_shoes}', (0, 90), scale=1.7, thickness=1, colorR=(255,0,255), colorT=(0, 0, 0))
    cvzone.putTextRect(img, f'Has cup: {has_cup}', (0, 130), scale=1.7, thickness=1, colorR=(255, 0, 255), colorT=(0, 0, 0))

    # Speak the text
    threading.Thread(target=speak, args=(text,)).start()

    cv2.imshow("img", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
