#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
import math
from geometry_msgs.msg import Twist
import time

def scan_callback(scan_data):
    global min_distance
    #Find minimum range
    min_value, min_index = min_range_index(scan_data.ranges)
    print ("\nthe minimum range value is: ", min_value)
    print ("the minimum range index is: ", min_index)
    min_distance = min_value

def min_range_index(ranges):
    global custom_range
    ranges = [x for x in ranges if not math.isnan(x)]
    custom_range = ranges[0:15]+ranges[345:360]
    return (min(custom_range), custom_range.index(min(custom_range)) )

def move(avoid_obstacle):
    #create a publisher to make the robot move
    global min_distance
    #velocity_publisher = rospy.Publisher("/cmd_vel_mux/input/teleop", Twist, queue_size=10)
    velocity_publisher = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    cmd_vel = Twist()
    
    loop_rate = rospy.Rate(100)
    while(True):
        if (avoid_obstacle):
            #behavior 1 
            cmd_vel.linear.x = .3
            cmd_vel.angular.z = 0.0
            while (min_distance>0.6):
                velocity_publisher.publish(cmd_vel)
                loop_rate.sleep()

            #behavior 2: force the robot rotate until it finds open space
            cmd_vel.linear.x = 0.0
            if min(custom_range[0:15])<min(custom_range[15:30]):
                cmd_vel.angular.z = -1.5
                while (min_distance<1):
                    velocity_publisher.publish(cmd_vel)
                    loop_rate.sleep()
            else:
                cmd_vel.angular.z = 1.5
                while (min_distance<1):
                    velocity_publisher.publish(cmd_vel)
                    loop_rate.sleep()




            
        

 
if __name__ == '__main__':
    
    #init new a node and give it a name
    rospy.init_node('scan_node', anonymous=True)
    #subscribe to the topic /scan. 
    rospy.Subscriber("scan", LaserScan, scan_callback)

    time.sleep(2)
    move(True)
    rotate(False)

    # spin() simply keeps python from exiting until this node is stopped
    # rospy.spin()
    try:
        rospy.spin()
    except rospy.ROSInterruptException:
        pass

     