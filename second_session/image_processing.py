#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np
import cv2


def readpath(path):
    # Read the file from the path and display it
    img = cv2.imread(pa/home/user1/catkin_ws/src/formacao/scripts/VisionAndRosWorkshop/second_session/road_1.jpegth)
    cv2.imshow('Original', img)
    return img


def edges(img):
    # Convert the image to grayscale
    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('Grayscale', img_gray)

    # Blur the image in order to facilitate edge detection
    img_blur = cv2.GaussianBlur(img_gray,(7, 7), 0)
    cv2.imshow('Blur', img_blur)

    # With Canny, detect edges
    img_edges = cv2.Canny(img_blur, 50, 150, apertureSize = 3)
    #plt.figure()
    #plt.imshow(img_edges, cmap = 'gray')
    #plt.show()

    cv2.waitKey(0)

    return img_edges

def ROI(img, vertices):
    # With the previously defined vertices, create a mask
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)

    # Joints the mask to the image
    img_masked = cv2.bitwise_and(img, mask)
    cv2.imshow('Masked', img_masked)
    cv2.waitKey(0)

    return img_masked

def houghlines(img, orimg):
    # Detect lines
    rho = 2
    theta = np.pi/180
    threshold = 40
    min_line_len = 100
    max_line_gap = 50
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len, maxLineGap=max_line_gap)
    img_line = np.zeros_like(orimg)
    
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img_line, (x1,y1), (x2,y2),  [255, 0, 0], 20)
    
    cv2.imshow('Lines', img_line)

    a = 1
    b = 1
    c = 0
    img_orig_line = cv2.addWeighted(orimg, a, img_line, b, c)

    cv2.imshow('Original with Lines', img_orig_line)

    cv2.waitKey(0)


    return img_orig_line


def binarize(img):
    # Binarize the image with Otsu Method

    img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    ret, img_bin = cv2.threshold(img_gray, 120, 255, cv2.THRESH_OTSU)   
    
    cv2.imshow('Binarized', img_bin)

    cv2.waitKey(0)
    return img_bin

def poly(img_bin):
    # With the binarized image, perform a polynomial fit in order to find the parameters

    height = img_bin.shape[0]
    vector = {"x": list(), "y": list()}
    x, y = vector["x"], vector["y"]

    for i, row in enumerate(img_bin):
        for j, pixel in enumerate(row):
            if pixel == 255:
                x.append(j)
                y.append(height - i)  # Top row should be largest and bottom row == 0

    # Robustness check
    assert len(y) == len(x), "Error: Vectors x and y are not of same length!"

    fit = np.polyfit(x=x, y=y, deg=2)


    return fit
