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
	tts.setLanguage("Portuguese")
	# Change the robot's posture to Crouch
	postureProxy.goToPosture("Stand", 0.5)

	#Hello
	
	tts.say("Olá eu sou o NAO!")
	Execute_Animation(hello_bye, 0.6)
	tts.say("Hoje vamos jogar o jogo do par ou ímpar. Conheces este jogo?")


	knows = raw_input("y - Knows the game \nn - Doesn't know the game\n->")
	if knows == 'y':
		tts.say("Se já sabes as regras do jogo só te preciso de explicar como vamos jogar. Em vez de usarmos os dez dedos vamos usar os nossos dois braços. Ou seja, as nossas respostas podem ser um ou dois braços!")
			
	if knows == 'n':
		tts.say("Este Jogo é simples. No início de cada jogo cada um de nós aposta se o número que vai sair é Par ou Ímpar, sendo que as apostas têm de ser diferentes. De seguida cada um de nos escolhe um número entre 1 e 2. Para isso levantamos o número de braços que queremos. No fim somamos as duas apostas e se essa soma for ímpar quem apostou ímpar ganha, se for par quem ganha é quem escolheu par.")

	tts.say("Vamos jogar cinco jogos. Quem ganhar mais jogos, GANHA!")
	tts.say("Vamos começar!")
	
	pointsRobot = 0
	pointsHuman = 0
	count = 0
	while count < 5:
		
		answer = raw_input("\npt - Points \nbr - Bet robot \nbh - Bet human \npw - Play wait \nph - Play hands\ne - End \n->")

		if answer == 'pt':
			tts.say("Está %s %s" % (pointsRobot, pointsHuman))
			print("Está %s %s" % (pointsRobot, pointsHuman))
			if pointsHuman > pointsRobot:
				tts.say("Contigo a ganhar")
				print("Contigo a ganhar")
			elif pointsRobot > pointsHuman:
				tts.say("Comigo a ganhar")
				print("Contigo a ganhar")
			elif pointsRobot == pointsHuman:
				tts.say("Estamos empatados")
				print("Estamos empatados")

		if answer == 'br':
			n = randint(0,1)
			if n == 0:
				tts.say("Eu aposto que vai ser um número par!")
				print("Eu aposto que vai ser um número par!")
				tts.say("Vou considerar a tua aposta como ímpar!")
				print("Vou considerar a tua aposta como ímpar!")
				
			elif n == 1:
				tts.say("Eu aposto que vai ser um número ímpar!")
				print("Eu aposto que vai ser um número ímpar!")
				tts.say("Vou considerar a tua aposta como par!")
				print("Vou considerar a tua aposta como par!")
			
		if answer == 'bh':
			tts.say("Qual é a tua aposta?")
			print("Qual é a tua aposta?")

			ha = raw_input("\n0 - Even \n1 - Odd\nHuman Answer ->")
			
			if ha == '0':
				tts.say("Como escolhes-te par eu vou apostar ímpar!")
				print("Como escolhes-te par eu vou apostar ímpar!")
			elif ha == '1':
				tts.say("Como escolhes-te ímpar eu vou apostar par!")
				print("Como escolhes-te ímpar eu vou apostar par!")

		if answer == 'pw':
			tts.say("1 2 3")
			print("1 2 3")
			
			pos = raw_input("\n1 - One hand up \n2 - Two hands up \nCheating robot Answer->")
			if pos == '1':
				Execute_Animation(rightHandUp, 1)
			if pos == '2':
				Execute_Animation(twoHandsUp, 1)
			
			win = raw_input("\nh - Human\nr - Robot\nWho won? ->")
			if win == 'h':
				pointsHuman += 1
				tts.say("Ganhaste!")
				print("Ganhaste!")
			if win == 'r':
				pointsRobot += 1
				tts.say("Ganhei!")
				print("Ganhei!")
			
			count += 1

		if answer == 'ph':
			tts.say("1 2 3")
			print("1 2 3")
			Execute_Animation(cheat, 1)

			pos = raw_input("\n1 - One hand up \n2 - Two hands up \nCheating robot Answer->")
			if pos == '1':
	   			Execute_Animation(cheatDown, 1)
			if pos == '2':
				Execute_Animation(cheatUp, 1)

			win = raw_input("\nh - Human\nr - Robot\nWho won? ->")
			if win == 'h':
				pointsHuman += 1
				tts.say("Ganhaste!")
				print("Ganhaste!")
			if win == 'r':
				pointsRobot += 1
				tts.say("Ganhei!")
				print("Ganhei!")
			
			count += 1

		if answer == 'e':
			exit()

	tts.say("Fim do jogo!")
	print("Fim do jogo!")

	if pointsHuman > pointsRobot:
		tts.say("Ganhaste! Parabéns!")
		print("Ganhaste! Parabéns!")
		Execute_Animation(animations.disappointed_pose, 0.6)
	elif pointsHuman < pointsRobot:
		tts.say("Ganhei!")
		print("Ganhei!")
		Execute_Animation(animations.winner2_pose, 0.6)
	
	time.sleep(5)
	tts.say("Adeus!")
	print("Adeus!")
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