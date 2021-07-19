#!/usr/bin/env python3
import rospy
from std_msgs.msg import Float64, Bool

# Creating a publisher

def talker(poly):
     # Defining the publisher, with the name of the topic, type of message, and number of queue
     pub_x2 = rospy.Publisher('x2', Float64, queue_size=10)
     pub_x1 = rospy.Publisher('x1', Float64, queue_size=10)
     pub_x0 = rospy.Publisher('x0', Float64, queue_size=10)

     # Initiating the node
     rospy.init_node('talker', anonymous=True)

     # Rate of messasges
     rate = rospy.Rate(10) # 10hz

     # While it's not shutdown, publish and wait to publish again
     while not rospy.is_shutdown():
         pub_x2.publish(poly[0])
         pub_x1.publish(poly[1])
         pub_x0.publish(poly[2])
         rate.sleep()
     


def callback(butn):
     # Defining the publisher
     pub_x2 = rospy.Publisher('x2', Float64, queue_size=10)
     pub_x1 = rospy.Publisher('x1', Float64, queue_size=10)
     pub_x0 = rospy.Publisher('x0', Float64, queue_size=10)
     rate = rospy.Rate(10) # 10hz
     # If btnm is true
     if butn.data: 
         pub_x2.publish(poly[0])
         pub_x1.publish(poly[1])
         pub_x0.publish(poly[2])
         rate.sleep()


# Creating a subscriber

def listener(fit): 
     # Creating a global variable to use on the callback function
     global poly
     poly = fit

     # Initiating the node
     rospy.init_node('phonetopc', anonymous=True)
   
     # Subscribing to the node used on ROS Mobile
     rospy.Subscriber("btn_press", Bool, callback)
   
     # Keep subscribing until the program is stoped
     rospy.spin()
