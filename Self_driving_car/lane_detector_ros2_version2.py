# https://www.youtube.com/watch?v=eLTLtUVuuy4

import cv2
import math
import numpy as np
import matplotlib.pyplot as plt

def find_canny(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # convert to gray image to reduce computational power
    blur_img = cv2.GaussianBlur(gray_img, (5, 5), 0) # blur img to reduce noise
    canny_img = cv2.Canny(blur_img, 50, 150) # find the edge
    return canny_img

def region_of_interest(img):
    height = img.shape[0]
    polygons = np.array([
        [(200, height), (1100, height), (550, 250)]
    ])
    mask = np.zeros_like(img) # turn the img into black
    mask = cv2.fillPoly(mask, polygons, 255) # fill the triangle with white
    masked_img = cv2.bitwise_and(img, mask) # crop the canny img into roi
    return masked_img

def average_slope_intercept(img, lines):
    left_fit = []
    right_fit = []
    for line in lines:
        x1, y1, x2, y2 = line.reshape(4)
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope, intercept = parameters

        if slope < 0:
            left_fit.append((slope, intercept))
        else:
            right_fit.append((slope, intercept))

    left_fit_average = np.average(left_fit, axis=0) if left_fit else None
    right_fit_average = np.average(right_fit, axis=0) if right_fit else None

    left_line = make_coordinates(img, left_fit_average) if left_fit_average is not None else None
    right_line = make_coordinates(img, right_fit_average) if right_fit_average is not None else None

    # Only include non-None lines
    output_lines = [line for line in [left_line, right_line] if line is not None]

    return np.array(output_lines, dtype=object)

def make_coordinates(img, line_parameters):
    slope, intercept = line_parameters
    # make the line start from bottom of the image (determine ROI)
    y1 = img.shape[0] # meaning y1 start from bottom of the image
    y2 = int(y1 * (3/5)) # meaning y2 is 3/5 of the y1 start from bottom of the image
    x1 = int((y1 - intercept) / slope)  # y=mx+b, x=(y-b)/m
    x2 = int((y2 - intercept) / slope)  # y=mx+b, x=(y-b)/m
    return np.array([x1, y1, x2, y2])

def display_lines(img, lines):
    line_img = np.zeros_like(img) # create a new black screen that same shape as original img
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line
            cv2.line(line_img, (x1, y1), (x2, y2), (255, 0, 0), 10)
    return line_img

def find_lane_center_point(img, lines, draw=True):
    # Initialize default trajectory points
    traj_top_point, traj_bottom_point = (0, 0), (0, 0)

    if lines is not None and len(lines) > 0:
        if len(lines) == 2:
            # If both lines are detected
            left_x1, left_y1, left_x2, left_y2 = lines[0]
            right_x1, right_y1, right_x2, right_y2 = lines[1]
        elif len(lines) == 1:
            # If only one line is detected, treat it as either left or right
            left_x1, left_y1, left_x2, left_y2 = lines[0]
            right_x1, right_y1, right_x2, right_y2 = lines[0]
        else:
            # Default values if no lines are detected
            return traj_top_point, traj_bottom_point

        # Calculate the trajectory points
        traj_top_point = (int((left_x2 + right_x2) / 2), int((left_y2 + right_y2) / 2))
        traj_bottom_point = (int((left_x1 + right_x1) / 2), int((left_y1 + right_y1) / 2))

        if draw:
            cv2.line(img, traj_bottom_point, traj_top_point, (0, 255, 255), 5)

    return traj_top_point, traj_bottom_point


def find_car_center_point(img, draw=True):
    x1_car = int(img.shape[1] / 2)  # img.shape[0] is height, img.shape[1] is width
    y1_car = int(img.shape[0])
    x2_car = int(img.shape[1] / 2)
    y2_car = int(y1_car * (4.5 / 5))
    if draw == True:
        cv2.line(img, (x1_car, y1_car), (x2_car, y2_car), (0, 0, 255), 5)

    return x1_car

def find_lane_curvature(x1,y1,x2,y2):
    offset_Vert=90# angle found by tan-1 (slop) is wrt horizontal --> This will shift to wrt Vetical

    if((x2-x1)!=0):
        slope = (y2-y1)/(x2-x1)
        y_intercept = y2 - (slope*x2) #y= mx+c
        anlgeOfinclination = math.atan(slope) * (180 / np.pi)#Conversion to degrees
    else:
        slope=1000#infinity
        y_intercept=0#None [Line never crosses the y axis]

        anlgeOfinclination = 90#vertical line

        #print("Vertical Line [Undefined slope]")
    if(anlgeOfinclination!=90):
        if(anlgeOfinclination<0):#right side
            angle_wrt_vertical = offset_Vert + anlgeOfinclination
        else:#left side
            angle_wrt_vertical = anlgeOfinclination - offset_Vert
    else:
        angle_wrt_vertical= 0#aligned
    return angle_wrt_vertical


def main_video():
    cap = cv2.VideoCapture("test2.mp4")
    while True:
        success, img = cap.read()

        # >>>>>>>>>> step2: find the edge of the lane >>>>>>>>>>
        canny_img = find_canny(img)

        # >>>>>>>>>> step3: find the roi >>>>>>>>>>
        cropped_img = region_of_interest(canny_img)

        # >>>>>>>>>> step4: find the line using Hough Transform >>>>>>>>>>
        rho = 2
        theta = np.pi / 180  # pi/180 is equal to 1 degree of precision
        thres = 100  # min number of vote needed to accepted a candidate line
        minLineLength = 40  # any line that less than 40 will be rejected
        maxLineGap = 5  # max distance btw 2 line will be connected as a single line
        lines = cv2.HoughLinesP(cropped_img, rho, theta, thres, np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)

        # >>>>>>>>>> step5: Optimization: find the average line for left and right side>>>>>>>>>>
        averaged_line = average_slope_intercept(img, lines)

        # >>>>>>>>>> step7: find lane and car centroid point >>>>>>>>>>
        traj_top_point, traj_bottom_point = find_lane_center_point(img, averaged_line)
        x1_car_point = find_car_center_point(img)

        # >>>>>>>>>> step8: find the error of distance and curvature  >>>>>>>>>>
        error_distance_x = -1000
        if error_distance_x != (0,0):
            error_distance_x = traj_bottom_point[0] - x1_car_point
        curvature = find_lane_curvature(traj_bottom_point[0], traj_bottom_point[1], traj_top_point[0],traj_top_point[1])
        print("error:", error_distance_x, ",   curvature:", curvature)

        # >>>>>>>>>> step10: display line >>>>>>>>>>
        line_img = display_lines(img, averaged_line)  # display line in black screen
        combo_img = cv2.addWeighted(img, 0.8, line_img, 1, 1)  # display line in original img

        cv2.imshow("video output", combo_img)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()
main_video()