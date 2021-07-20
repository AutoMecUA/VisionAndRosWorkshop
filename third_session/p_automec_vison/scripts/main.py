#!/usr/bin/env python3

from cv_bridge import CvBridge
from image_processing import *
from ros_pubandsub import *
from sensor_msgs.msg import Image

def image_get(image):
    global cv_image
    bridge = CvBridge()
    cv_image = bridge.imgmsg_to_cv2(image, desired_encoding='passthrough')
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    global see_image
    see_image = True

def circular(img):
    img_bin = binarize(img)
    vertices = np.array([[(450, 520),(450,350),(550,350),(850,520)]])
    img_roi = ROI(img_bin, vertices)
    #fit = poly(img_roi)
    return img_roi

def main():

    global cv_image
    rospy.init_node('Robot_Send', anonymous=True)
    rospy.Subscriber('/p_automec/camera/rgb/image_raw', Image, image_get)

    global see_image
    see_image = False
    while not rospy.is_shutdown():
        if see_image == False:
            continue
        img = cv_image
        circular(img)
        #listener(fit)
        rospy.Rate(20).sleep()
   


    
    




if __name__ == "__main__":
    main()
 