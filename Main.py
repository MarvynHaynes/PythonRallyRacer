# File: Main.py
# Author: Marvyn Haynes
# CST8333-350 - Advanced Languages
# Assignment 05
# Date: 11/24/14
# Summary: This is the second protoype of my racing car game.  This file serves as the main python script
# to run the game, calling various methods from classes.py, process.py and screenWrite.py.
# Scattered throughout each of these files contain commented out code for testing purposes as I am 
# testing the import of race track using python instead of using 3rd party libraries.
#
# -=MAJOR CHANGES=-
# 1. Main.py: 
#	- Track no longer uses tiled images.  Instead, all positions are tracked using xy-coordinates.
#	- Added scoreboard and time counter.
#	- Added testing features for positioning and troubleshooting.
#	- Moved I/O to Main.py to write time counter value when user wins to file 'highscores.txt'
# 2. classes.py
#	- CalcCarCoords method added to classes.py.
#	- Adjusted user controls for smoother gameplay
#	- Fixed all out of bounds issues
#	- Added option for different opponent speed range to represent difficulty.  Can be passed from Main.py when drawing oppCar objects
#	- Removed MultiThreading to oppCar class (causing issues)
# 3. Process.py
#	- Added markers on the racetrack that tracks when a car object passes over it. If all 4 are marked, 1 lap is added to object car
# 
#
# -=Problems=-
# 1. Car gets stuck in middle of track
# 2. Steering is reversed
#
# -=TODO=-
# 1. Need to add title page and menu
# 2. Need to implement ready, set go at start of round
# 3. Need to implement rounds
# 4. Need to add sound effects and music
# 5. Add collision detection between cars

#######################################################
# IMPORTS
#######################################################
import pygame, sys, screenWrite, threading
from classes import *
from process import process
import time
import pickle


#######################################################
# INITIALIZERS
#######################################################

pygame.init()
pygame.font.init()

#Shows list of builtin fonts (Troubleshooting)
#print sorted (pygame.font.get_fonts())

#Screen variables
scrWidth, scrHeight = 1024, 768
background = pygame.image.load("images/tracks/TestTrack3.png")
screen = pygame.display.set_mode((scrWidth, scrHeight))

#Colors
White = (255, 255, 255)
Black = (0, 0, 0)
Red = (255, 0, 0)
Green = (0, 255, 0)
Yellow = (255, 204, 51)
Blue = (0, 102, 255)

#Stopwatch Timer variables
milliseconds = 0
seconds = 0
minutes = 0
hours = 0
TimerOn = False

#Assures time is kept evenly across all PCs
clock = pygame.time.Clock()

#Helps with keeping track of seconds using FPS variable (if totalframes % fivescondinterval = 0 then ...) 
FPS = 24
fivesecondinterval  = FPS * 5
totalframes = 0

writeRecords = False

#How many laps to complete
lapNum = 5

#######################################################
# INITIALIZE CAR OBJECTS
#######################################################

allCars = []
playerCar = UserCar((255,640), 26, 50, "images/red_car_track2.png")
allCars.append(playerCar)

oppCar1_Green = oppCar((255,600), 26, 50, "images/oppCar_green.png")
allCars.append(oppCar1_Green)

oppCar2_Yellow = oppCar((255,664), 26, 50, "images/oppCar_yellow.png")
allCars.append(oppCar2_Yellow)

oppCar3_Blue = oppCar((255,684), 26, 50, "images/oppCar_blue.png")
allCars.append(oppCar3_Blue)

#######################################################
# TIMER METHOD
#######################################################

def LaunchTimer():
	global milliseconds, seconds, minutes, hours
	#pygame.time.wait(10)
	milliseconds = milliseconds + 1
	if milliseconds == 100:
		seconds = seconds + 1
		milliseconds = milliseconds - 100
	if seconds == 60:
		minutes = minutes + 1
		seconds = seconds - 60
	if minutes == 60:
		hours = hours + 1
		minutes = minutes - 60
       

while True:
	process(screen, allCars)	
	#LOGIC_BEGIN

	playerCar.motion(scrWidth, scrHeight)

	#Opponents
	#Last 2 values signify: 
	#1. Spacing between (car x,y route, best used between current ranges) 
	#2. Car speed: 1 (slowest) - 5 (fastest)
	oppCar1_Green.draw_oppCar(scrWidth, scrHeight, 96, 1)
	oppCar2_Yellow.draw_oppCar(scrWidth, scrHeight, 32, 1)
	oppCar3_Blue.draw_oppCar(scrWidth, scrHeight, 64, 4)
	
	screen.blit(background, (0,0))
	LaunchTimer()


	#LOGIC_END		


#######################################################
#DRAW SCOREBOARD 
#######################################################
	scoreboard = pygame.draw.rect(screen,(0,0,0),(250, 370, 525,100))
	screenWrite.text_to_screen(screen,"Player Lap:", scoreboard.left + 10, scoreboard.top + 10, color = Red)
	screenWrite.text_to_screen(screen, playerCar.lap, scoreboard.left + 10, scoreboard.top + 30)
	screenWrite.text_to_screen(screen,"Opponent 1:", scoreboard.left + 150, scoreboard.top + 10, color = Green)
	screenWrite.text_to_screen(screen, oppCar1_Green.lap, scoreboard.left + 150, scoreboard.top + 30)
	screenWrite.text_to_screen(screen,"Opponent 2:", scoreboard.right - 250, scoreboard.top + 10, color = Yellow)
	screenWrite.text_to_screen(screen, oppCar2_Yellow.lap, scoreboard.right - 250, scoreboard.top + 30)
	screenWrite.text_to_screen(screen,"Opponent 3:", scoreboard.right - 125, scoreboard.top + 10, color = Blue)
	screenWrite.text_to_screen(screen, oppCar3_Blue.lap, scoreboard.right - 125, scoreboard.top + 30)

	screenWrite.text_to_screen(screen, "Timer:", ((scoreboard.left + scoreboard.right)/2) - 125, scoreboard.bottom - 33, size = 20)
	screenWrite.text_to_screen(screen, minutes, ((scoreboard.left + scoreboard.right)/2) - 45, scoreboard.bottom - 30, size = 20, font_type = 'impact')
	screenWrite.text_to_screen(screen, ":", ((scoreboard.left + scoreboard.right)/2) - 25, scoreboard.bottom - 30, size = 20, font_type = 'impact')
	screenWrite.text_to_screen(screen, seconds, ((scoreboard.left + scoreboard.right)/2) - 10, scoreboard.bottom - 30, size = 20, font_type = 'impact')
	screenWrite.text_to_screen(screen, ":", ((scoreboard.left + scoreboard.right)/2) +10 , scoreboard.bottom - 30, size = 20, font_type = 'impact')
	screenWrite.text_to_screen(screen, milliseconds, ((scoreboard.left + scoreboard.right)/2) + 20, scoreboard.bottom - 30, size = 20, font_type = 'impact')
	
	pygame.draw.line(screen, (255, 255, 255), (340, 561), (340, 747), 20)

#######################################################
#TESTING AND TROUBLESHOOTING
#######################################################
	
	# Display debug info on screen

	# screenWrite.text_to_screen(screen, ("Speed:",playerCar.speed), 3, 3, size = 25, color = (255, 255, 0))
	# screenWrite.text_to_screen(screen, ("Dir:",playerCar.direction), 3, 43, size = 25, color = (0, 255, 255))
	# screenWrite.text_to_screen(screen, ("Lap:",playerCar.lap), 3, 103, size = 30, color = (255, 64, 196))

	# screenWrite.text_to_screen(screen, ("X:",playerCar.position[0]), scrWidth - 160, 3, size = 25, color = (145, 255, 0))
	# screenWrite.text_to_screen(screen, ("Y:",playerCar.position[1]), scrWidth - 160, 43, size = 25, color = (145, 255, 0))

	# screenWrite.text_to_screen(screen, ("Mark1:",playerCar.trackMark1), 32, scrHeight - 92, color = Black)
	# screenWrite.text_to_screen(screen, ("Mark2:",playerCar.trackMark2), 32, scrHeight - 72, color = Black)
	# screenWrite.text_to_screen(screen, ("Mark3:",playerCar.trackMark3), 32, scrHeight - 52, color = Black)
	# screenWrite.text_to_screen(screen, ("Mark4:",playerCar.trackMark4), 32, scrHeight - 32, color = Black)

	# screenWrite.text_to_screen(screen, ("X:",oppCar1_Green.position[0]), scrWidth - 160, 83, size = 25, color = (255, 29, 0))
	# screenWrite.text_to_screen(screen, ("Y:",oppCar1_Green.position[1]), scrWidth - 160, 123, size = 25, color = (255, 29, 0))
	# screenWrite.text_to_screen(screen, ("Dir:",oppCar1_Green.direction), scrWidth - 160, 163, size = 25, color = (255, 29, 0))
	# screenWrite.text_to_screen(screen, ("Speed:",oppCar1_Green.speed), scrWidth - 160, 183, size = 25, color = (255, 255, 0))

	# screenWrite.text_to_screen(screen, ("Lap:",oppCar1_Green.lap), scrWidth - 160, 223, size = 30, color = (255, 64, 196))

	# screenWrite.text_to_screen(screen, ("Mark1:",oppCar1_Green.trackMark1), scrWidth - 128, scrHeight - 92)
	# screenWrite.text_to_screen(screen, ("Mark2:",oppCar1_Green.trackMark2), scrWidth - 128, scrHeight - 72)
	# screenWrite.text_to_screen(screen, ("Mark3:",oppCar1_Green.trackMark3), scrWidth - 128, scrHeight - 52)
	# screenWrite.text_to_screen(screen, ("Mark4:",oppCar1_Green.trackMark4), scrWidth - 128, scrHeight - 32)

	###Test inner boundaries
	
	# #left
	# track_left = pygame.draw.line(screen, (255, 247, 0), (246, 259), (246, 529))
	# #top
	# pygame.draw.line(screen, (255, 247, 0), (246, 259), (777, 259))
	# #right
	# pygame.draw.line(screen, (255, 247, 0), (777, 259), (777, 529))
	# #bottom
	# pygame.draw.line(screen, (255, 247, 0), (777, 529), (246, 529))

	# #Track Mark right
	# pygame.draw.line(screen, (255, 247, 0), (805, 410), (995, 410))
	# #Track Mark top
	# pygame.draw.line(screen, (255, 247, 0), (510, 40), (510, 235))
	# #Track Mark left
	# pygame.draw.line(screen, (255, 247, 0), (34, 410), (222, 410))
	# #Track Mark bottom
	# pygame.draw.line(screen, (255, 247, 0), (340, 555), (340, 747))


	#Draws all images from classes group on screen
	BaseCar.allsprites.draw(screen)
	

### CHECK FOR WINNER

	if playerCar.lap == lapNum and oppCar1_Green.lap < lapNum and oppCar2_Yellow.lap < lapNum and oppCar3_Blue.lap < lapNum:
		#pygame.draw.rect(screen,(0,0,0),(145, (scrHeight /2) - 5, 100,100))
		screenWrite.text_to_screen(screen, "YOU ARE A WINNER!!!", 150, (scrHeight /2), size = 60)
		if writeRecords == False:
			recordedTime = str(minutes) + ":" + str(seconds) + ":" + str(milliseconds)
			pickle.dump (recordedTime, open ("highscores.txt", "a"))
			writeRecords = True

	elif playerCar.lap < lapNum and oppCar1_Green.lap == lapNum and oppCar2_Yellow.lap < lapNum and oppCar3_Blue.lap < lapNum:
		screenWrite.text_to_screen(screen, "OPPONENT 1 IS A WINNER!!!", 50, (scrHeight /2), color = Green, size = 60)

	elif playerCar.lap < lapNum and oppCar1_Green.lap < lapNum and oppCar2_Yellow.lap == lapNum and oppCar3_Blue.lap < lapNum:
		screenWrite.text_to_screen(screen, "OPPONENT 2 IS A WINNER!!!", 50, (scrHeight /2), color = Yellow, size = 60)

	elif playerCar.lap < lapNum and oppCar1_Green.lap < lapNum and oppCar2_Yellow.lap < lapNum and oppCar3_Blue.lap == lapNum:
		screenWrite.text_to_screen(screen, "OPPONENT 3 IS A WINNER!!!", 50, (scrHeight /2), color = Blue, size = 60)
		

	#makes sure everything is redrawn		
	pygame.display.flip()
	clock.tick(FPS)
	totalframes += 1
	#For testing FPS 
	#if totalframes % fivesecondinterval == 0:



