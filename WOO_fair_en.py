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
from random import randint
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

#poses
import animations.winner2_pose
import animations.disappointed_pose

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
	nao_PORT = 42675

	myBroker = ALBroker("myBroker",        
		"0.0.0.0",   # listen to anyone
    	0,           # find a free port and use it
    	nao_IP,         # parent broker IP
    	nao_PORT)       # parent broker port)

	global motionProxy
	motionProxy = ALProxy("ALMotion", nao_IP, nao_PORT)

	postureProxy = ALProxy("ALRobotPosture", nao_IP, nao_PORT)
	tts    = ALProxy("ALTextToSpeech", nao_IP, nao_PORT)
	tts.setLanguage("English")
	# Change the robot's posture to Crouch
	postureProxy.goToPosture("Stand", 0.5)

	#Hello
	
	tts.say("Hello I'm NAO!")
	Execute_Animation(hello_bye, 0.6)
	tts.say("Today we are going to play the even or odd game. Do you know this game?")


	knows = raw_input("y - Knows the game \nn - Doesn't know the game\n->")
	if knows == 'y':
		tts.say("If you already know the rules of the game, I just need to explain how we are going to play. Instead of using the ten fingers we are going to use our two arms. That is, our answers can be one or two arms!")
			
	if knows == 'n':
		tts.say("This game is simple. At the beginning of each game, each of us bets on whether the number to come out is Even or Odd, and the bets must be different. Then each of us chooses a number between 1 and 2. For this, we raise the number of arms we want. In the end, we add the two bets and if that sum is odd who bet odd wins, if it is even who wins is who chose even.")

	tts.say("We will play five games. Whoever wins the most games, WINS!")
	tts.say("Let's start!")
	
	pointsRobot = 0
	pointsHuman = 0
	count = 0
	while count < 5:
		answer = raw_input("\npt - Points \nbr - Bet robot \nbh - Bet human \np - Play\ne - End \n->")

		if answer == 'pt':
			tts.say("%s %s" % (pointsRobot, pointsHuman))
			print("%s %s" % (pointsRobot, pointsHuman))
			if pointsHuman > pointsRobot:
				tts.say("With you to win")
				print("With you to win")
			if pointsRobot > pointsHuman:
				tts.say("With me winning")
				print("With me winning")
			if pointsRobot == pointsHuman:
				tts.say("We are tied")
				print("We are tied")

		if answer == 'br':
			n = randint(0,1)
			if n == 0:
				tts.say("I bet it will be an even number!")
				print("I bet it will be an even number!")
				tts.say("I will consider your bet as odd!")
				print("I will consider your bet as odd!")
			if n == 1:
				tts.say("I bet it will be an odd number!")
				print("I bet it will be an odd number!")
				tts.say("I will consider your bet as a even!")
				print("I will consider your bet as a even!")
			
		if answer == 'bh':
			tts.say("What is your bet?")
			print("What is your bet?")
			ha = raw_input("\n0 - Even \n1 - Odd\nHuman Answer ->")
			
			if ha == '0':
				tts.say("How you choose even I will bet odd!")
				print("How you choose even I will bet odd!")
			if ha == '1':
				tts.say("How you choose odd I'll bet even!")
				print("How you choose odd I'll bet even!")

		if answer == 'p':
			tts.say("1 2 3")
			print("1 2 3")
			n = randint(0,1)
			if n == 0:
				Execute_Animation(rightHandUp, 1)
			if n == 1:
				Execute_Animation(twoHandsUp, 1)

			win = raw_input("\nh - Human\nr - Robot\nWho won? ->")
			if win == 'h':
				pointsHuman += 1
				tts.say("You won!")
				print("You won!")
			if win == 'r':
				pointsRobot += 1
				tts.say("I won!")
				print("I won!")
			
			count += 1

		if answer == 'e':
			exit()

	tts.say("End of the game!")
	print("End of the game!")

	if pointsHuman > pointsRobot:
		tts.say("You won! Congratulations!")
		print("You won! Congratulations!")
		Execute_Animation(animations.disappointed_pose, 0.6)
	if pointsHuman < pointsRobot:
		tts.say("I won!")
		print("I won!")
		Execute_Animation(animations.winner2_pose, 0.6)
	
	time.sleep(5)
	tts.say("Bye!")
	print("Bye!")
	Execute_Animation(hello_bye, 0.6)
	exit()

if __name__ == "__main__":

	
	try:
		main()
		rospy.spin()

    	except rospy.ROSInterruptException:
        	print
        	print "Interrupted by user, shutting down"
        	myBroker.shutdown()
        	sys.exit(0)