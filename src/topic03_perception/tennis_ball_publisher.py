#!/usr/bin/env python
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

bridge = CvBridge()
cap = cv2.VideoCapture('/home/tariqul/catkin_ws/src/ros_essentials_cpp/src/topic03_perception/video/tennis-ball-video.mp4')
#cap = cv2.VideoCapture(0)
#print(cap.isOpened())


def talker():

    rospy.init_node('tennis_ball_pub', anonymous=True)
    pub = rospy.Publisher('tennis_ball', Image, queue_size=10)
    rate = rospy.Rate(10) 

    while not rospy.is_shutdown():
         try:
            ret,frame = cap.read()
            ros_img = bridge.cv2_to_imgmsg(frame,encoding='bgr8')
            rospy.loginfo("Publishing Frames")

            pub.publish(ros_img)
            rate.sleep()
         except rospy.ROSInterruptException:
            pass

    print('Done')
    cap.release()
    cv2.destroyAllWindows()
         
         

        
if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
       pass

    print("SHUTTING DOWN")
