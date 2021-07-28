#!/usr/bin/env python3
import cv2
import geometry_msgs.msg
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge()  # Create a converter class instance to use in the imageReceivedCallback
publisher_twist = rospy.Publisher('/p_automec/cmd_vel', geometry_msgs.msg.Twist,
                                  queue_size=10)  # Define the publisher of the car velocity


def imageReceivedCallback(image_msg):
    # Convert received image message to an OpenCV image for processing
    image_cv = bridge.imgmsg_to_cv2(image_msg, desired_encoding='passthrough')
    image_cv = cv2.cvtColor(image_cv,
                            cv2.COLOR_RGB2BGR)  # Gazebo works with RGB and OpenCV works with BGR, conversion is needed
    image_gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    ret, image_binarized = cv2.threshold(image_gray, 240, 255, cv2.THRESH_BINARY)

    # Process image to estimate the best driving angle and speed

    ### YOUR CODE COMES HERE###

    # find left point
    height, width = image_binarized.shape
    row = int(height/2)
    left_col = None
    right_col = None

    for col in range(0, int(width/2)): # search for left point
        pixel_value = image_binarized[row, col]
        # print("col=" + str(col) + ' pixel value = ' + str(pixel_value))
        if pixel_value == 255:  # found white!!!
            left_col = col
            cv2.line(image_cv, (col, row - 8), (col, row + 8), (0, 0, 255), 3)
            cv2.line(image_cv, (col- 8, row ), (col+ 8, row ), (0, 0, 255), 3)
            break

    for col in range(width-1, int(width/2), -1):  # search for right point
        pixel_value = image_binarized[row, col]
        if pixel_value == 255:  # found white!!!
            right_col = col
            cv2.line(image_cv, (col, row - 8), (col, row + 8), (255, 0, 0), 3)
            cv2.line(image_cv, (col - 8, row), (col + 8, row), (255, 0, 0), 3)
            break

    if left_col != None and right_col != None:
        central_col = int((left_col + right_col) / 2)
    else:
        central_col = int(width / 2)

    cv2.line(image_cv, (central_col, row - 8), (central_col, row + 8), (0, 255, 0), 3)
    cv2.line(image_cv, (central_col - 8, row), (central_col + 8, row), (0, 255, 0), 3)


    # compute delta_x
    delta_x = int(width/2) - central_col

    # Linear and angular velocity values
    linear_velocity = 0.4
    # PID controller ... only P for now
    angular_velocity = delta_x * 0.01

    # Create Twist message to define linear and angular velocity and send it
    twist_msg = geometry_msgs.msg.Twist()
    twist_msg.linear.x = linear_velocity
    twist_msg.angular.z = angular_velocity

    # Publish twist_msg message
    publisher_twist.publish(twist_msg)

    # Show received image
    cv2.namedWindow('image received', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('image received', image_cv)
    cv2.namedWindow('imageBin', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('imageBin', image_binarized)
    cv2.namedWindow('imageGrey', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('imageGrey', image_gray)
    cv2.waitKey(10)


def main():
    rospy.init_node('driver_mriem', anonymous=False)  # Initialization
    rospy.Subscriber('/p_automec/camera/rgb/image_raw', Image,
                     imageReceivedCallback)  # Subscriber of the image received from gazebo
    rospy.spin()  # Continues running the code


if __name__ == "__main__":
    main()
