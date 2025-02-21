# https://www.youtube.com/watch?v=eLTLtUVuuy4

import cv2
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
        x1, y1, x2, y2 = line.reshape(4) # original line is in 2d array, need to reshape into 1d array
        parameters = np.polyfit((x1, x2), (y1, y2), 1) # polyfit return slope and y-intercept of line
        # print(parameters)
        slope = parameters[0]
        intercept = parameters[1]

        if slope < 0:                           # if slope is negative, meaning it is on the left side
            left_fit.append((slope, intercept))
        else:                                   # if slope is positive, meaning it is on the right side
            right_fit.append((slope, intercept))
        # print("left_fit: ", left_fit, "        right_fit", right_fit)

    # find the average of left lines and right lines, making them become 1 line for both side
    left_fit_average = np.average(left_fit, axis=0)
    right_fit_average = np.average(right_fit, axis=0)
    # print("left_fit_avg: ", left_fit_average, "        right_fit_avg", right_fit_average)

    # find the coordinate of left line and right line
    left_line = make_coordinates(img, left_fit_average)
    right_line = make_coordinates(img, right_fit_average)
    return np.array([left_line, right_line])

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



def main_img():
    # >>>>>>>>>> step1: read the img >>>>>>>>>>
    image = cv2.imread("test_image.jpg")
    lane_image = np.copy(image)
    # plt is used to find the coordinate of the roi (eg. triangular 3 points)
    # plt.imshow(lane_image)
    # plt.show()

    # >>>>>>>>>> step2: find the edge of the lane >>>>>>>>>>
    canny_img = find_canny(lane_image)

    # >>>>>>>>>> step3: find the roi >>>>>>>>>>
    cropped_img = region_of_interest(canny_img)

    # >>>>>>>>>> step4: find the line using Hough Transform >>>>>>>>>>
    rho = 2
    theta = np.pi/180 # pi/180 is equal to 1 degree of precision
    thres = 100 # min number of vote needed to accepted a candidate line
    minLineLength = 40 # any line that less than 40 will be rejected
    maxLineGap = 5 # max distance btw 2 line will be connected as a single line
    lines = cv2.HoughLinesP(cropped_img, rho, theta, thres, np.array([]), minLineLength=minLineLength, maxLineGap=maxLineGap)

    # >>>>>>>>>> step5: Optimization: find the average line for left and right side>>>>>>>>>>
    averaged_line = average_slope_intercept(lane_image, lines)

    # >>>>>>>>>> step6: display line >>>>>>>>>>
    line_img = display_lines(lane_image, averaged_line) # display line in black screen
    combo_img = cv2.addWeighted(lane_image, 0.8, line_img, 1, 1) # display line in original img

    # >>>>>>>>>> step7: show the output >>>>>>>>>>
    cv2.imshow("img", combo_img)
    cv2.waitKey(0)

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

        # >>>>>>>>>> step6: display line >>>>>>>>>>
        line_img = display_lines(img, averaged_line)  # display line in black screen
        combo_img = cv2.addWeighted(img, 0.8, line_img, 1, 1)  # display line in original img

        cv2.imshow("video output", combo_img)
        if cv2.waitKey(1) & 0xff == ord("q"):
            break
    cv2.destroyAllWindows()

# main_img()
main_video()