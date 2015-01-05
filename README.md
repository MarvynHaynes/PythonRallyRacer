PythonRallyRacer
================
Author: Marvyn Haynes
Date: 11/24/14

A prototype top-view racing game created for a school project built using Python and PyGame.


Objective
------------
Be the first car to successfully complete 5 laps around the racetrack to win.  User controls the car by using the arrow direction keys.


Quick Summary
-------------
This is my first attempt of creating a Python app and creating a racing game. 

In this project contains 4 python scripts and 1 folder:

•Main.py - The main file that runs the racing game. Sets up the race car and references to various objects and movement definition by calling methods and fuctions in the below classes.

• Classes.py - Defines user and opponent car objects and behaviors

• Process.py - Defines arrow key input behavior from user

• screenWrite.py - Contains a function to write text to screen

• Images folder - contains car images and racetrack (*.png)

Scattered throughout each of these files contain commented out code for testing purposes as I am 
testing the import of race track using python instead of using 3rd party libraries.  This project is a work in progress and needs major improvement.


-=MAJOR CHANGES=-
1. Main.py: 
	- Track no longer uses tiled images.  Instead, all positions are tracked using xy-coordinates.
	- Added scoreboard and time counter.
	- Added testing features for positioning and troubleshooting.
	- Moved I/O to Main.py to write time counter value when user wins to file 'highscores.txt'

2. classes.py
	- CalcCarCoords method added to classes.py.
	- Adjusted user controls for smoother gameplay
	- Fixed all out of bounds issues
	- Added option for different opponent speed range to represent difficulty.  Can be passed from Main.py when drawing oppCar objects
	- Removed MultiThreading to oppCar class (causing issues)

3. Process.py
	- Added markers on the racetrack that tracks when a car object passes over it. If all 4 are marked, 1 lap is added to object car


-=Problems=-
1. Car gets stuck in middle of track
2. Steering is reversed (left and right arrow keys)

-=TODO=-
1. Need to add title page and menu
2. Need to implement ready, set go at start of round
3. Need to implement rounds
4. Need to add sound effects and music
5. Add collision detection between cars
