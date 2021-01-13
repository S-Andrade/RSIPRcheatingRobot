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

import OneHandUp
import TwoHandsUp
import HelloBye
import Cheat


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

	data = []

	# change IP and Port accordingly
	#nao_IP = '192.168.0.101'
	#nao_PORT = 9559

	nao_IP = '127.0.0.1'
	nao_PORT = 36663

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
	asr = ALProxy("ALSpeechRecognition", nao_IP, nao_PORT)
	asr.setLanguage("English")
	vocabulary = ["one", "two"]
	asr.setVocabulary(vocabulary, False)
	# Change the robot's posture to Crouch
	postureProxy.goToPosture("StandInit", 0.5)

	#Hello
	
	tts.say("\\style=didactic\\ Hello \\pau=1000\\  I'm Pedro!")
	Execute_Animation(HelloBye, 0.5)
	tts.say("Today we are going to play the even or odd game. Do you know this game?")

	knows = raw_input("y - Knows the game \nn - Doesn't know the game\n->")
	if knows == 'y':
		tts.say("If you already know the rules of the game, I just need to explain how we are going to play.  \\pau=1000\\ Instead of using the ten fingers we are going to use our two arms. That is, our answers can be one or two arms!")
	if knows == 'n':
		tts.say("This game is simple.\\pau=1000\\ At the beginning of each game,\\pau=100\\ each of us bets on whether the number to come out is Even \\pau=100 \\or \\pau=100\\ Odd, \\pau=100\\ and the bets must be different. \\pau=1000\\ Then each of us chooses a number between 1 and 2.\\pau=1000\\ For this,\\pau=100\\ we raise the number of arms we want.\\pau=1000\\  In the end,\\pau=100\\ we add the two bets \\pau=100\\and if that sum is odd \\pau=100\\ who bet odd wins, \\pau=1000\\ if it is even \\pau=100\\ who wins is who chose even.")

	tts.say("We will play three games. Whoever wins the most games, WINS!")
	tts.say("Let's start!")
	
	pointsRobot = 0
	pointsHuman = 0
	count = 0
	while count < 3:
		answer = raw_input("\npt - Points \nbr - Bet robot \nbh - Bet human \np - Play\ne - End \n->")

		if answer == 'pt':
			tts.say("%s %s" % (pointsRobot, pointsHuman))
			print("%s %s" % (pointsRobot, pointsHuman))
			if pointsHuman > pointsRobot:
				tts.say("With you winning")
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
				tts.say("\\rspd=90\\I bet it will be an even number!")
				print("I bet it will be an even number!")
				tts.say("I will consider your bet as odd!")
				print("I will consider your bet as odd!")
			if n == 1:
				tts.say("I bet it will be an odd number!")
				print("I bet it will be an odd number!")
				tts.say("I will consider your bet as a even!")
				print("I will consider your bet as a even!")
			
		if answer == 'bh':
			tts.say("\\rspd=90\\ What is your bet?")
			print("What is your bet?")
			ha = raw_input("\n0 - Even \n1 - Odd\nHuman Answer ->")
			
			if ha == '0':
				tts.say("\\rspd=90\\ Becouse you choose even \\pau=1000\\ I will bet odd!")
				print("How you choose even I will bet odd!")
			if ha == '1':
				tts.say("\\rspd=90\\ Becouse you choose odd \\pau=1000\\ I'll bet even!")
				print("How you choose odd I'll bet even!")

		if answer == 'p':
			tts.say("1 \\pau=1000\\ 2 \\pau=1000\\ 3")
			print("1 2 3")
			n = randint(0,1)
			asr.subscribe(ip)
			memProxy = ALProxy("ALMemory", nao_IP, nao_PORT)
			memProxy.subscribeToEvent('WordRecognized',nao_IP,'wordRecognized')
			time.sleep(2)
			asr.unsubscribe(ip)
			data=memProxy.getData("WordRecognized")
			print( "data: %s" % data )

			if n == 0:
				Execute_Animation(OneHandUp, 0.4)
			if n == 1:
				Execute_Animation(TwoHandsUp, 0.4)

			win = raw_input("\nh - Human\nr - Robot\nWho won? ->")
			if win == 'h':
				pointsHuman += 1
				tts.say("\\style=neutral\\ \\rspd=90\\ You won! \\style=didactic\\")
				print("You won!")
			if win == 'r':
				pointsRobot += 1
				tts.say("\\style=joyful\\ \\rspd=90\\  I won! \\style=didactic\\")
				print("I won!")
			
			count += 1

		if answer == 'e':
			exit()

	tts.say("\\style=didactic\\ \\rspd=90\\End of the game!")
	print("End of the game!")

	if pointsHuman > pointsRobot:
		tts.say("\\style=neutral\\ You won! Congratulations! \\style=didactic\\")
		print("You won! Congratulations!")
		Execute_Animation(animations.disappointed_pose, 0.6)
	if pointsHuman < pointsRobot:
		tts.say("\\style=joyful\\ I won! \\style=didactic\\")
		print("I won!")
		Execute_Animation(animations.winner2_pose, 0.6)
	
	time.sleep(5)
	tts.say("Bye!")
	print("Bye!")
	Execute_Animation(HelloBye, 0.4)
	motionProxy.rest()
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
