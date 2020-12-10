#!/home/won/.pyenv/versions/rospy3/bin/python
import math
import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class SelfDrive:
    def __init__(self, publisher):
        self.publisher = publisher

    def lds_callback(self, scan):
        turtle_vel = Twist()
        scan_Value = average(scan.ranges[225:315])
        scan_Value_Top = average(scan.ranges[270:315])
        scan_Value_Bottom = average(scan.ranges[225:270])

        if scan_Value >= 0.195 and scan_Value <= 0.22:
            turtle_vel.linear.x = 0.18
            self.stop(self,scan.ranges[0])
            self.publisher.publish(turtle_vel)
        elif scan_Value > 0.22:
            self.right_Top_Down_Comparison(scan, scan_Value_Top, scan_Value_Bottom, scan.ranges[0])
        else:
            self.left_Top_Down_Comparison(scan, scan_Value_Top, scan_Value_Bottom, scan.ranges[0])

    def stop(self, scan):
        turtle_vel = Twist()
        if scan.ranges[0] < 0.3 and scan.ranges[0] > 0.1:
            print(scan.ranges[0], "stop")
            turtle_vel.linear.x = 0
            turtle_vel.angular.z = math.pi / 2
            self.publisher.publish(turtle_vel)

    def right_Top_Down_Comparison(self, scan_Value_Top, scan_Value_Bottom, scan_Value_Front):
        turtle_vel = Twist()
        if (scan_Value_Top >= scan_Value_Bottom):
            turtle_vel.angular.z = -(math.pi / 3)
            turtle_vel.linear.x = 0.14
            self.stop(self, scan_Value_Front)
            self.publisher.publish(turtle_vel)
        else:
            turtle_vel.angular.z = (math.pi / 9)
            self.publisher.publish(turtle_vel)
            turtle_vel.linear.x = 0.18
            self.stop(self, scan_Value_Front)
            self.publisher.publish(turtle_vel)

    def left_Top_Down_Comparison(self, scan_Value_Top, scan_Value_Bottom, scan_Value_Front):
        turtle_vel = Twist()
        if (scan_Value_Top >= scan_Value_Bottom):
            turtle_vel.angular.z = -(math.pi / 9)
            turtle_vel.linear.x = 0.18
            self.stop(self, scan_Value_Front)
            self.publisher.publish(turtle_vel)
        else:
            turtle_vel.angular.z = (math.pi / 3)
            turtle_vel.linear.x = 0.14
            self.stop(self, scan_Value_Front)
            self.publisher.publish(turtle_vel)

def average(list):
    return (sum(list) / len(list))


def main():
    rospy.init_node('self_drive')
    publisher = rospy.Publisher('cmd_vel', Twist, queue_size=1)
    driver = SelfDrive(publisher)
    subscriber = rospy.Subscriber('scan', LaserScan,
                                  lambda scan: driver.lds_callback(scan))
    rospy.spin()

if __name__ == "__main__":
    main()
