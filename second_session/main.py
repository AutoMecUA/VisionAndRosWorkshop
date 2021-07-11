#!/usr/bin/env python3


from image_processing import *
from ros_pubandsub import *

# Linear not used in this workshop

#def lineari(img):
#    img_edges = edges(img)
#    vertices = np.array([[(180,520),(450,300),(520,300),(850,520)]])
#    img_roi = ROI(img_edges, vertices)
#    img_line = houghlines(img_roi, img)
#    return img_line

def circular(img):
    img_bin = binarize(img)
    vertices = np.array([[(450, 520),(450,350),(550,350),(850,520)]])
    img_roi = ROI(img_bin, vertices)
    fit = poly(img_roi)
    return fit

def main():
    path = 'road_1.jpeg'
    img = readpath(path)
    fit = circular(img)
    listener(fit)
    #talker(fit)
    




if __name__ == "__main__":
    main()
 