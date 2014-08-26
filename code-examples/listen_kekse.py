#!/usr/bin/env python
import rospy
import sys
from std_msgs.msg import String

def callback(data):
    sys.stdout.write('.')
    sys.stdout.flush() 
    pass
    
def listener():
    rospy.init_node('listen_kekse', anonymous=True)
    rospy.Subscriber("kekse", String, callback)
    # spin() simply keeps python from exiting until this node is stopped
    print("listening..")
    rospy.spin()


listener()
