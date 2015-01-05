# File: process.py
# Author: Marvyn Haynes
# CST8333-350 - Advanced Languages
# Assignment 05
# Date: 11/24/14
# Summary: This file contains functionality for player movement, marking sections cars has passed over and exiting the game. 
# I/O has been removed to Main.py


import pygame, sys
import pickle
import time
import datetime

def process(screen, allCars):

	#PROCESSES_BEGIN

	#loops through every type of event get
	for event in pygame.event.get():
		# once it detects python.quit event
		if event.type == pygame.QUIT:
			pygame.quit() #game quits
			sys.exit() #the system exists
		if not hasattr(event, 'key'): continue
		keyDown = event.type == pygame.KEYDOWN		
		if event.key == pygame.K_RIGHT: 
			allCars[0].k_right = (keyDown * 5)

		elif event.key == pygame.K_LEFT: 
			allCars[0].k_left = (keyDown * 5)

		elif event.key == pygame.K_UP: 
			allCars[0].k_up = (keyDown * 2)

		elif event.key == pygame.K_DOWN: 
			allCars[0].k_down = abs(keyDown * 2)

		
	#Below tracks any car objects that passes over each of the 4 objects.  
	#RightTrack Marker
	for carObj in allCars:
		if carObj.position[0] > 777 and carObj.position[0] < 1024: #Marker length
				if carObj.position[1] < 455 and carObj.position[1] > 405 : #Marker thickness					
					carObj.trackMark1 = True				
		
		#TopTrack Marker		
		if carObj.position[1] > 32 and carObj.position[1] < 259:
				if carObj.position[0] > 500 and carObj.position[0] < 550 :
					carObj.trackMark2 = True			
			
		#LeftTrack Marker		
		if carObj.position[0] > 0 and carObj.position[0] < 246:
				if carObj.position[1] < 450 and carObj.position[1] > 400 :
					carObj.trackMark3 = True				

		#BottomTrack Marker		
		if carObj.position[1] > 529 and carObj.position[1] < 768:
				if carObj.position[0] > 330 and carObj.position[0] < 370 :
					#Checks if previous markers have been marked to ensure car objects are not just starting before marking 
					if carObj.trackMark1 and carObj.trackMark2 and carObj.trackMark3 == False:
						carObj.trackMark4 = False
					elif carObj.trackMark1 and carObj.trackMark2 and carObj.trackMark3 == True: 
						carObj.trackMark4 = True
						

		#If all 4 markers are driven over, add 1 lap
		if carObj.trackMark1 and carObj.trackMark2 and carObj.trackMark3 and carObj.trackMark4 == True:
			carObj.lap = carObj.lap + 1
			carObj.trackMark1 = carObj.trackMark2 = carObj.trackMark3 = carObj.trackMark4 = False
			break


	#PROCESSES_END