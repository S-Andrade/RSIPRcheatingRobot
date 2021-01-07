#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
######
# Author = Elmira Yadollahi
# Date = 05.12.2019
######


import codecs
import time
import re
import random
import threading 

# Debug
import rospy
import sys
import motion
import almath
import math

# NAO Brokers
from naoqi import ALProxy 
from naoqi import ALModule
from naoqi import ALBroker


# Sample Animations
import animations.winner2_pose
import animations.disappointed_pose

import OneHandUp
import TwoHandsUp
import HelloBye


def Execute_Animation(pose, factorSpeed = 1.0):
    """ Recieves the animation and the speed, send the movement to the robot
    """

    times = changeSpeed(pose.times, factorSpeed)
    motionProxy.post.angleInterpolationBezier(pose.names, times, pose.keys)


def changeSpeed(times, factor):
    """ It changes the speed of predefined times for each pose movement
    """

    for i in xrange(len(times)):
        times[i] = [x / float(factor) for x in times[i]]

    return times


def main():
    rospy.init_node('animation_execution_sample')

	# change IP and Port accordingly
    nao_IP = '192.168.0.100'
    nao_PORT = 9559

    myBroker = ALBroker("myBroker",        
        "0.0.0.0",   # listen to anyone
        0,           # find a free port and use it
        nao_IP,         # parent broker IP
        nao_PORT)       # parent broker port)

    global motionProxy
    motionProxy = ALProxy("ALMotion", nao_IP, nao_PORT)
    #motionProxy.rest()
    postureProxy = ALProxy("ALRobotPosture", nao_IP, nao_PORT)
	
    postureProxy.goToPosture("StandInit", 0.5)
    
    Execute_Animation(HelloBye, 0.5)
    #postureProxy.goToPosture("StandInit", 0.5)
	

if __name__ == "__main__":

	
	try:
		main()
		rospy.spin()

    	except rospy.ROSInterruptException:
        	print
        	print "Interrupted by user, shutting down"
        	myBroker.shutdown()
        	sys.exit(0)