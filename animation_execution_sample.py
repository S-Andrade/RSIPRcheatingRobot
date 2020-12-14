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
import animations.embarassed_seated_pose
import animations.scratchHead_seated_pose
import animations.thinking1_pose
import animations.thinking8_seated_pose
import animations.monster_seated_pose
import animations.disappointed_seated_pose
import animations.crying_seated_pose
import animations.crying_pose


# Idle Movement Animations
import animations.lookHand_seated_pose
import animations.relaxation_seated_pose
import animations.scratchHand_seated_pose
import animations.scratchHead_seated_pose
import animations.introduction_pose
import animations.winner_pose
import animations.winner2_pose

import hello_bye
import rightHandUp
import twoHandsUp
import cheat
import cheatUp
import cheatDown


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
	nao_IP = '127.0.0.1'
	nao_PORT = 33829

	myBroker = ALBroker("myBroker",        
		"0.0.0.0",   # listen to anyone
    	0,           # find a free port and use it
    	nao_IP,         # parent broker IP
    	nao_PORT)       # parent broker port)

	global motionProxy
	motionProxy = ALProxy("ALMotion", nao_IP, nao_PORT)

	postureProxy = ALProxy("ALRobotPosture", nao_IP, nao_PORT)
	tts    = ALProxy("ALTextToSpeech", nao_IP, nao_PORT)
	
	# Change the robot's posture to Crouch
	postureProxy.goToPosture("Stand", 0.5)

	#Hello
	Execute_Animation(hello_bye, 0.6)

	time.sleep(2)

	#One hand Up
	Execute_Animation(rightHandUp, 0.7)

	time.sleep(2)

	#Two hands Up
	Execute_Animation(twoHandsUp, 0.8)
	 
	time.sleep(2)

	#Cheating Up
	Execute_Animation(cheat, 0.9)
 	Execute_Animation(cheatUp, 1)

	time.sleep(2)

	#Cheating Down
	Execute_Animation(cheat, 1.1)
 	Execute_Animation(cheatDown, 1.2)
	
	time.sleep(2)

	#GoodBye
	Execute_Animation(hello_bye, 1.3)

if __name__ == "__main__":

	
	try:
		main()
		rospy.spin()

    	except rospy.ROSInterruptException:
        	print
        	print "Interrupted by user, shutting down"
        	myBroker.shutdown()
        	sys.exit(0)