#! /usr/bin/env python3

import rospy
import std_msgs
import ondo.msg

import sys
import time
import NASCORX_System.device.L218 as L218

if __name__=='__main__':
    # initialize parameters
    # ---------------------
    nodename = 'l218_status'
    topicname = 'l218'
    rospy.init_node(nodename)
    host = rospy.get_param('~host')
    port = rospy.get_param('~port')
    rate = rospy.get_param('~rate')

    # setup devices
    # -------------
    try:
        lakeshore = L218.l218(host, port)
    except OSError as e:
        rospy.logerr("{e.strerror}. host={host}".format(**locals()))
        sys.exit()

    # setup ros
    # ---------
    pub = rospy.Publisher(topicname, ondo.msg.l218_values, queue_size=1)

    # start loop
    # ----------
    while not rospy.is_shutdown():
        ret = lakeshore.measure()

        d = ondo.msg.l218_values()
        d.ch1_value = ret[0]
        d.ch2_value = ret[1]        
        d.ch3_value = ret[2]
        d.ch4_value = ret[3]
        d.ch5_value = ret[4]
        d.ch6_value = ret[5]
        d.ch7_value = ret[6]
        d.ch8_value = ret[7]
        pub.publish(d)

        time.sleep(rate)
        continue
