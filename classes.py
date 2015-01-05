# File: classes.py
# Author: Marvyn Haynes
# CST8333-350 - Advanced Languages
# Assignment 05
# Date: 11/24/14
# Summary: This file contains all the classes for the different racecar objects, functions and properties.
# Both userCar and oppCar instances passes through calcCarCoords method to calculate position, projectery and movement 
# for all car objects.  
# 

import pygame, threading, math, screenWrite
from random import randint


#Using Base class will declare all variables needed to create images and move car objects

class BaseCar(pygame.sprite.Sprite, pygame.Rect):
#class BaseCar(pygame.Rect):
	width, height = 0, 0
	position = (0,0)
	maxFwdSpeed = 10
	maxRwdSpeed = 0

	#helps with collision detection and draws image with one command
	allsprites = pygame.sprite.Group()
	
	def __init__(self, position, width, height, image_string):
		
		pygame.Rect.__init__(self, BaseCar.position[0], BaseCar.position[1], BaseCar.width, BaseCar.height)
		pygame.sprite.Sprite.__init__(self)
		BaseCar.allsprites.add(self)
		self.orig_image = pygame.image.load(image_string)
		self.image = self.orig_image
		
		#Gets dimensions of car image and makes rectangle boundaries
		self.rect = self.image.get_rect()

		self.width = width
		self.height = height

		self.position = position
		self.speed = self.direction = 0
		self.k_left = self.k_right = self.k_down = self.k_up = self.decelerate = 0
		self.lap = 0
		self.trackMark1 = self.trackMark2 = self.trackMark3 = self.trackMark4 = self.outOfBounds = None


		

class UserCar(BaseCar):

	carList = pygame.sprite.Group()
	def __init__(self, position, width, height, image_string):
		
		BaseCar.__init__(self, position, width, height, image_string)
		self.direction = -90

	def motion(self, scrWidth, scrHeight):
		#Calculate input from process class (process.py)
		if self.k_up == 0:
			self.k_up = self.k_up - 0.1 #To simulate gas pedal release
			self.speed += (self.k_up - self.k_down)
		else:
			self.speed += (self.k_up - self.k_down)		
		self.speed += (self.k_up - self.k_down)	
		if self.speed > self.maxFwdSpeed:
			self.speed = self.maxFwdSpeed
		if self.speed < self.maxRwdSpeed:
			self.speed = self.maxRwdSpeed
		self.direction += (self.k_right - self.k_left)
		
		#Pass instance to calculate car movement
		#calcCarCoords(self)

		
		#Set Top Screen Boundaries
		if self.x < 0:
			self.speed = -(self.speed)
		#Set Bottom Screen Boundaries
		elif self.x > scrWidth - 10:
			self.speed = -(self.speed)


		#Set Left Side Boundaries
		elif self.y < 0:		
			self.speed = -(self.speed)
		#Set Right Side Boundaries		
		elif self.y > scrHeight - 10:
			self.speed = -(self.speed)

		#SET Middle Boundaries
		elif self.x > 246 and self.x < 777:
			if self.y > 259 and self.y < 529:
				self.speed = -(self.speed)
				#Issue with car when user drives to the bottom side of the inner grass area
		
		#Pass instance to calculate coordinates
		calcCarCoords(self)

		#Transform car direction to self.diretion using original image
		self.image = pygame.transform.rotate(self.orig_image, self.direction)
		#Move car
		self.rect.center = self.position


class oppCar(BaseCar, threading.Thread):
	oppCarList = []
	def __init__(self, position, width, height, image_string):

		
		BaseCar.__init__(self, position, width, height, image_string)
		oppCar.oppCarList.append(self)



	def draw_oppCar(self, scrWidth, scrHeight, grid_dist, speedNum):
		#Assigns car speed.  Generates random numbers with specific min, max values.
		for car in oppCar.oppCarList:		
			if speedNum == 1:
				self.speed = (randint(1, 3))
			elif speedNum == 2:
				self.speed = (randint(1, 4))
			elif speedNum == 3:
				self.speed = (randint(1, 5))
			elif speedNum == 4:
				self.speed = (randint(1, 6))
			elif speedNum == 5:
				self.speed = (randint(1, 7))
			else:
				self.speed = 0		
			
			#Assigns car grid position. Used to align cars correctly while racing on track
			self.grid_dist = grid_dist

			#Logic for driving bottom track portion
			if self.position[1] > 529 + grid_dist and self.position[1] < scrHeight - grid_dist:
				if self.position[0] > 32 and self.position[0] < scrWidth - grid_dist:
					self.direction = -90

			#Logic for driving right track portion
			if self.position[0] > 777 + grid_dist and self.position[0] < scrWidth - grid_dist:
				if self.position[1] > 32 and self.position[1] < scrHeight - 32:
					self.direction = 0

			#Top Track position
			if self.position[1] > 32 and self.position[1] < 259 - grid_dist:
				if self.position[0] > 32 and self.position[0] < scrWidth - grid_dist:
					self.direction = 90

			#Left Track Position
			if self.position[0] > 32 and self.position[0] < 246 - grid_dist:
				if self.position[1] > 32 and self.position[1] < scrHeight - (grid_dist + 32):
					self.direction = 180

		
			#Boundaries incase if Computer controlled objects stray off path
			#Set Top Screen Boundaries
			if self.x < 32:
				self.direction = 225 
				calcCarCoords(self)
			#Set Bottom Screen Boundaries
			elif self.x > scrWidth - 32:
				self.direction = 25 
				calcCarCoords(self)				

			#Set Left Side Boundaries
			elif self.y < 32:		
			 	self.direction = 100
			 	calcCarCoords(self) 
			#Set Right Side Boundaries			
			elif self.y > scrHeight - 64:
				self.direction = 285 
			 	calcCarCoords(self)

		 	#Set Inner Boundaries
			elif self.x > 246 and self.x < 777:
				if self.y > 259 and self.y < 529:
					self.speed = 0

			#Pass instance to calculate coordinates
			calcCarCoords(self)
			
			#Transform car direction to self.diretion using original image
			self.image = pygame.transform.rotate(self.orig_image, self.direction)
			#Move car
			self.rect.center = self.position
	
def calcCarCoords(self):
			#Calculate coordinates for car movement
			
			self.x, self.y = self.position

			#Calculation using radius to determine projectory
			rad = self.direction * math.pi / 180			

			self.x += -self.speed*math.sin(rad)
			self.y += -self.speed*math.cos(rad)

			self.position = (self.x, self.y)
			return self				


