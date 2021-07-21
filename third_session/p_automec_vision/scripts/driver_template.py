#!/usr/bin/env python3
import cv2
import geometry_msgs.msg
import rospy
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

bridge = CvBridge() # Create a converter class instance to use in the imageReceivedCallback
publisher_twist = rospy.Publisher('/p_automec/cmd_vel', geometry_msgs.msg.Twist, queue_size=10) # Define the publisher of the car velocity


def imageReceivedCallback(image_msg):

    # Convert received image message to an OpenCV image for processing
    image_cv = bridge.imgmsg_to_cv2(image_msg, desired_encoding='passthrough')
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR) # Gazebo works with RGB and OpenCV works with BGR, conversion is needed

    # Process image to estimate the best driving angle and speed

    ### YOUR CODE COMES HERE###

    # Linear and angular velocity values
    linear_velocity = 0.2
    angular_velocity = 1.1

    # Create Twist message to define linear and angular velocity and send it
    twist_msg = geometry_msgs.msg.Twist()
    twist_msg.linear.x = linear_velocity
    twist_msg.angular.z = angular_velocity

    # Publish twist_msg message
    publisher_twist.publish(twist_msg)

    # Show received image
    cv2.namedWindow('image received', cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow('image received', image_cv)
    cv2.waitKey(10)


def main():

    rospy.init_node('driver', anonymous=True) # Initialization
    rospy.Subscriber('/p_automec/camera/rgb/image_raw', Image, imageReceivedCallback) # Subscriber of the image received from gazebo
    rospy.spin() # Continues running the code


if __name__ == "__main__":
    main()
 