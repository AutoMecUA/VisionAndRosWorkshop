from image_processing import *

def linear(img):
    img_edges = edges(img)
    vertices = np.array([[(180,520),(450,300),(520,300),(850,520)]])
    img_roi = ROI(img_edges, vertices)
    img_line = houghlines(img_roi, img)
    return img_line

def circular(img):
    img_bin = binarize(img)
    vertices = np.array([[(450, 520),(450,350),(550,350),(850,520)]])
    img_roi = ROI(img_bin, vertices)
    fit = poly(img_roi)
    return fit

def main():
    path = 'road_1.jpeg'
    img = readpath(path)
    img_line = linear(img)
    fit = circular(img)
    




if __name__ == "__main__":
    main()
 