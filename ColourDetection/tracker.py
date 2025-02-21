import cv2

# Global variables for trackbar values
hueLow = 0
hueHigh = 0
satLow = 0
satHigh = 0
valLow = 0
valHigh = 0

# Callback functions for trackbars
def onTrack1(value):
    global hueLow
    hueLow = value
    print("Hue Low:", hueLow)

def onTrack2(value):
    global hueHigh
    hueHigh = value
    print("Hue High:", hueHigh)

def onTrack3(value):
    global satLow
    satLow = value
    print("Saturation Low:", satLow)

def onTrack4(value):
    global satHigh
    satHigh = value
    print("Saturation High:", satHigh)

def onTrack5(value):
    global valLow
    valLow = value
    print("Value Low:", valLow)

def onTrack6(value):
    global valHigh
    valHigh = value
    print("Value High:", valHigh)

# Function to create trackbars
def create_trackbars(window_name):
    cv2.namedWindow(window_name)
    cv2.createTrackbar("Hue Low", window_name, 10, 179, onTrack1)
    cv2.createTrackbar("Hue High", window_name, 20, 179, onTrack2)
    cv2.createTrackbar("Saturation Low", window_name, 10, 255, onTrack3)
    cv2.createTrackbar("Saturation High", window_name, 250, 255, onTrack4)
    cv2.createTrackbar("Value Low", window_name, 10, 255, onTrack5)
    cv2.createTrackbar("Value High", window_name, 250, 255, onTrack6)

# Function to get trackbar values
def get_trackbar_values():
    return hueLow, hueHigh, satLow, satHigh, valLow, valHigh
