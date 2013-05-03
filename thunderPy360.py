#!/usr/bin/python

# Copyright 2013, Justin Walrath
# Script was modified from pygame.org (http://www.pygame.org/docs/ref/joystick.html)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import pygame					#Handles the interface to the xbox and display
import os						#Determines if in sudo or not.
import sys						#Handles the command line entry point environment
import time						#Library that determines time.
import usb.core				#Libraries to control the usb interface.

# Define some colors
BLACK  = (  0,   0,   0)
WHITE  = (255, 255, 255)
RED    = (255,   0,   0)
GREEN  = (  0, 255,   0)
YELLOW = (255, 255,   0)

#This class is the controls for the ThunderPy missile launcher.
class launchControl():
	def __init__(self):
		self.dev = usb.core.find(idVendor=0x2123, idProduct=0x1010)
		if self.dev is None:
			raise ValueError('Launcher not found.')
		if self.dev.is_kernel_driver_active(0) is True:
			self.dev.detach_kernel_driver(0)
		self.dev.set_configuration()

	def moveUp(self):
		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x02,0x00,0x00,0x00,0x00,0x00,0x00]) 

	def moveDown(self):
		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x01,0x00,0x00,0x00,0x00,0x00,0x00])

	def moveLeft(self):
		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x04,0x00,0x00,0x00,0x00,0x00,0x00])

	def moveRight(self):
		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x08,0x00,0x00,0x00,0x00,0x00,0x00])

	def stopMove(self):
		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x20,0x00,0x00,0x00,0x00,0x00,0x00])

	def launchRocket(self):
		self.dev.ctrl_transfer(0x21,0x09,0,0,[0x02,0x10,0x00,0x00,0x00,0x00,0x00,0x00])

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
	def __init__(self):
		self.reset()
		self.font = pygame.font.Font(None, 20)

	def l_print(self, screen, textString):
		textBitmap = self.font.render(textString, True, BLACK)
		screen.blit(textBitmap, [self.x, self.y])
		self.y += self.line_height
        
	def reset(self):
		self.x = 10
		self.y = 10
		self.line_height = 15
        
	def indent(self):
		self.x += 10
        
	def unindent(self):
		self.x -= 10

#------------------------------------------------------------------------------
#It all begins here
if __name__ == '__main__':
	if not os.geteuid() == 0:
		sys.exit("Please run as sudo.")

#Start up the missile launcher
launcher = launchControl()

#Initialize the pygame libraries
pygame.init()
 
# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("ThunderPy 360")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

#concurrency variables
moving = False
hatDirection = -1
firing = False
fireLength = 0
alert = "Stationary"

screenColor = WHITE

# -------- Main Program Loop -----------
while done == False:
	# EVENT PROCESSING STEP
	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
        
	# DRAWING STEP
	# First, clear the screen to white. Don't put other drawing commands
	# above this, or they will be erased with this command.
	screen.fill(screenColor)
	textPrint.reset()

	# Get count of joysticks
	joystick_count = pygame.joystick.get_count()

	#textPrint.l_print(screen, "Number of joysticks: {}".format(joystick_count) )
	#textPrint.indent()
    
	# For each joystick:
	for i in range(joystick_count):
		joystick = pygame.joystick.Joystick(i)
		joystick.init()
    
		buttons = joystick.get_numbuttons()
		#textPrint.l_print(screen, "Number of buttons: {}".format(buttons) )
		#textPrint.indent()

		#Only going to be using the "A" button
		#for i in range( buttons ):
		button = joystick.get_button(0)
		if firing:	
			if (pygame.time.get_ticks() - fireLength) > 2000:
				screenColor = YELLOW
				alert = "Reloading"
			if (pygame.time.get_ticks() - fireLength) > 4000:
				firing = False
				launcher.stopMove()
				screenColor = WHITE
				alert = "Stationary"
		else:
			if button == 1:
				firing = True
				fireLength = pygame.time.get_ticks()
				launcher.launchRocket()
				screenColor = RED
				alert = "Launching Missile"
		#textPrint.l_print(screen, "Button {:>2} value: {}".format(0,button) )
		button = joystick.get_button(7)
		#textPrint.l_print(screen, "Button {:>2} value: {}".format(7,button) )
		if button == 1:
			done = True
		#textPrint.unindent()
            
		# Hat switch. All or nothing for direction, not like joysticks.
		# Value comes back in an array.
		hats = joystick.get_numhats()
		#textPrint.l_print(screen, "Number of hats: {}".format(hats) )
		#textPrint.indent()

		#Commented out since there is only 1 d-pad
		#for i in range( hats ):
		hat = joystick.get_hat(0)
		if not firing:
			if moving:
				if hat[hatDirection] == 0:
					launcher.stopMove()
					moving = False
					screenColor = WHITE
					alert = "Stationary"
			else:
				if hat[0] != 0:
					if hat[0] == -1: #left
						launcher.moveLeft()
						moving = True
						hatDirection = 0
						screenColor = GREEN
						alert = "Moving Left"
					if hat[0] == 1: #Right
						launcher.moveRight()
						moving = True
						hatDirection = 0
						screenColor = GREEN
						alert = "Moving Right"
				elif hat[1] != 0:
					if hat[1] == -1: #Down
						launcher.moveDown()
						moving = True
						hatDirection = 1
						screenColor = GREEN
						alert = "Moving Down"
					if hat[1] == 1: #Up
						launcher.moveUp()
						moving = True
						hatDirection = 1
						screenColor = GREEN
						alert = "Moving Up"
		#textPrint.l_print(screen, "Hat {} value: {}".format(0, str(hat)) )
		textPrint.l_print(screen, alert)
		#textPrint.unindent()  
		#textPrint.unindent()

    
	# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()

	# Limit to 20 frames per second
	clock.tick(60)

	if done:
		launcher.stopMove()
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
pygame.quit()
