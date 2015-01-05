# File: screenWrite.py
# Author: Marvyn Haynes
# CST8333-350 - Advanced Languages
# Assignment 05
# Date: 11/24/14
# Summary: This file contains a class to write text objects to screen. Leaving here for clarity of code.

import pygame

#Stick with common fonts across different OS
def text_to_screen(screen, text, x, y, size = 17, color = (255, 255, 255), 
	font_type = 'arialblack'):
	
	try:

		text = str(text)
		font = pygame.font.SysFont(font_type, size)
		text = font.render(text, True, color)
		screen.blit(text, (x, y))


	except Exception, e:
		print 'Font Error: Font not found'
		raise e
	
