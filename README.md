# VisionAndRosWorkshop
First session has the intent to help people develop a basic understanding of the OpenCV library in Python.


# How to run

To setup gazebo, run:
    
    roslaunch p_automec_bringup gazebo.launch

To spawn a p_automec player, run:

    roslaunch p_automec_bringup bringup.launch

To run the vision code, run:

    rosrun p_automec_vision driver_template.py

# Installation

### turtlebot3 
  
    git clone https://github.com/ROBOTIS-GIT/turtlebot3.git
    git clone https://github.com/ROBOTIS-GIT/turtlebot3_msgs.git      

Also, you must add this to your .bashrc 

    export TURTLEBOT3_MODEL=waffle_pi


