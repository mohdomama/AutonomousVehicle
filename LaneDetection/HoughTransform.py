import cv2
import os
import imutils
import numpy as np

def get_canny(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 100)
    return canny


def get_segment(frame):
    height = frame.shape[0]
    width = frame.shape[1] 
    print(height, width)
    polygons = np.array([
                        [(int(0.2 * width), int(height)), (int(0.8 * width), int(height)), (int(0.5 * width), int(0.1 * height))],
                ])
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, polygons, 255)
    segment = cv2.bitwise_and(frame, mask)
    return segment

def calculate_coordinates(frame, parameters):
    slope, intercept = parameters
    # Sets initial y-coordinate as height from top down (bottom of the frame)
    y1 = frame.shape[0]
    # Sets final y-coordinate as 150 above the bottom of the frame
    y2 = int(y1 - 150)
    # Sets initial x-coordinate as (y1 - b) / m since y1 = mx1 + b
    x1 = int((y1 - intercept) / slope)
    # Sets final x-coordinate as (y2 - b) / m since y2 = mx2 + b
    x2 = int((y2 - intercept) / slope)
    return np.array([x1, y1, x2, y2])

def visualize_lines(frame, lines):
    # Creates an image filled with zero intensities with the same dimensions as the frame
    lines_visualize = np.zeros_like(frame)
    # Checks if any lines are detected
    if lines is not None:
        for x1, y1, x2, y2 in lines:
            # Draws lines between two coordinates with green color and 5 thickness
            cv2.line(lines_visualize, (x1, y1), (x2, y2), (0, 255, 0), 5)
    return lines_visualize

def calculate_lines(frame, lines):
    # Empty arrays to store the coordinates of the left and right lines
    left = []
    right = []
    # Loops through every detected line
    for line in lines:
        # Reshapes line from 2D array to 1D array
        x1, y1, x2, y2 = line.reshape(4)
        # Fits a linear polynomial to the x and y coordinates and returns a vector of coefficients which describe the slope and y-intercept
        parameters = np.polyfit((x1, x2), (y1, y2), 1)
        slope = parameters[0]
        y_intercept = parameters[1]
        # If slope is negative, the line is to the left of the lane, and otherwise, the line is to the right of the lane
        if slope < 0:
            left.append((slope, y_intercept))
        else:
            right.append((slope, y_intercept))
    # Averages out all the values for left and right into a single slope and y-intercept value for each line
    left_avg = np.average(left, axis = 0)
    right_avg = np.average(right, axis = 0)
    # Calculates the x1, y1, x2, y2 coordinates for the left and right lines
    left_line = calculate_coordinates(frame, left_avg)
    right_line = calculate_coordinates(frame, right_avg)
    return np.array([left_line, right_line])

def main():
    DIR = 'Data/'
    for filename in os.listdir(DIR):
        try:
            image = cv2.imread(DIR + filename)
            image = imutils.resize(image, height=360)
            canny = get_canny(image)
            segment = get_segment(canny)

            hough = cv2.HoughLinesP(segment, 2, np.pi / 180, 100, np.array([]), minLineLength = 100, maxLineGap = 50)
            lines = calculate_lines(image, hough)
            # Visualizes the lines
            lines_visualize = visualize_lines(image, lines)



            cv2.imshow("hough", lines_visualize)
            # Overlays lines on frame by taking their weighted sums and adding an arbitrary scalar value of 1 as the gamma argument
            output = cv2.addWeighted(image, 0.9, lines_visualize, 1, 1)
            # Opens a new window and displays the output frame
            cv2.imshow("output", output)
            cv2.imshow('image', image)
            cv2.waitKey(0)
        except:
            pass
        

main()
 