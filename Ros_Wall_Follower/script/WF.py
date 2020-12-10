#!/usr/bin/env python

import math
import rospy
from geometry_msgs.msg import Twist

from sensor_msgs.msg import LaserScan


class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher
    
    def lds_callback(self, scan):
        turtle_vel = Twist()
        Scan_Value = average(scan.ranges[225:315])
        Scan_Value_Top = average(scan.ranges[270:315])
        Scan_Value_Bottom = average(scan.ranges[225:270])
        Scan_Value_Middle = average(scan.ranges[265:275])
        print(Scan_Value)
  
        if Scan_Value >= 0.20 and Scan_Value <= 0.25:
            turtle_vel.linear.x = 0.14
            print("go")
            check_SVM(Scan_Value_Middle)

        if (scan.ranges[10:-10] == 0.12):
            turtle_vel.linear.x = 0
            turtle_vel.angular.z = (math.pi / 5)

        elif Scan_Value > 0.25:
            turtle_vel.angular.z = -(math.pi / 8)
            turtle_vel.linear.x = 0.14 
            print("right go")
            check_SVM(Scan_Value_Middle)

            if(Scan_Value_Top > Scan_Value_Bottom):
                turtle_vel.angular.z = -(math.pi / 8)
                turtle_vel.linear.x = 0.14 
                print("right go")    
                check_SVM(Scan_Value_Middle)
            else:
                turtle_vel.angular.z = math.pi / 4 
                turtle_vel.linear.x = 0.14
                print("left go")
                check_SVM(Scan_Value_Middle)

        elif Scan_Value < 0.2:
            turtle_vel.angular.z = math.pi / 4 
            turtle_vel.linear.x = 0.14
            print("left go")
            check_SVM(Scan_Value_Middle)

            if(Scan_Value_Top > Scan_Value_Bottom):
                turtle_vel.angular.z = -(math.pi / 8)
                turtle_vel.linear.x = 0.14 
                print("right go")
                check_SVM(Scan_Value_Middle)
            else:
                turtle_vel.angular.z = -(math.pi / 8)
                turtle_vel.linear.x = 0.14 
                print("right go")
                check_SVM(Scan_Value_Middle)

        self.publisher.publish(turtle_vel)

def average(list):
    return (sum(list) / len(list))

def check_SVM(scaned_value):
    if(scaned_value > 3):
        turtle_vel.angular.z = -(math.pi / 4)

def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()

