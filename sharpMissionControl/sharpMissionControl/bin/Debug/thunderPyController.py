#!/usr/bin/python

# Copyright 2013, Justin Walrath
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

import os				#Determines if in sudo or not.
import sys				#Handles the command line entry point environment
import time				#Library that determines time.
import usb.core		#Libraries to control the usb interface.

##
# Controller class for manipulating the Thunder class missile launcher.
#
# @author: Justin Walrath <walrathjaw@gmail.com>
# @since: 4/9/2013
##
class launchControl():
	def __init__(self):
#Id codes were found running dmesg in ubuntu
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

#Indefinite commands - useful for gui and controller
	def controlContin(self, command):
		#Left
		if command == "-l" or command == "-left":
			self.moveLeft()
		#Right
		if command == "-r" or command == "-right":
			self.moveRight()
		#Up
		if command == "-u" or command == "-up":
			self.moveUp()
		#Down
		if command == "-d" or command == "-down":
			self.moveDown()
		#Fire
		if command == "-f" or command == "-fire":
			self.control(command, 2)
		#Stop
		if command == "-s" or command == "-stop":
			self.stopMove()

#Timed commands
	def control(self, command, mov_time):
		#Left
		if command == "-l" or command == "-left":
			stop = time.time() + mov_time
			while time.time() < stop:
				self.moveLeft()
			self.stopMove()
			print "done"
		#Right
		if command == "-r" or command == "-right":
			stop = time.time() + mov_time
			while time.time() < stop:
				self.moveRight()
			self.stopMove()
			print "done"
		#Up
		if command == "-u" or command == "-up":
			stop = time.time() + mov_time
			while time.time() < stop:
				self.moveUp()
			self.stopMove()
			print "done"
		#Down
		if command == "-d" or command == "-down":
			stop = time.time() + mov_time
			while time.time() < stop:
				self.moveDown()
			self.stopMove()
			print "done"
		#Fire
		if command == "-f" or command == "-fire":
			self.launchRocket()
			stop = time.time() + 3.7		#Pause for 2 seconds to make sure it fires.
			i = 2
			while time.time() < stop:
				i
			#self.launchRocket()
			self.stopMove()
			print "done"

#It all begins here
if __name__ == '__main__':
	if not os.geteuid() == 0:
		sys.exit("Please run as sudo.")
	if len(sys.argv) == 3:
		if sys.argv[1] == "-c" or sys.argv[1] == "-continue":
			launchControl().controlContin(sys.argv[2])
		else:
			launchControl().control(sys.argv[1], float(sys.argv[2]))
	elif len(sys.argv) == 2:
		if sys.argv[1] == "-f" or sys.argv[1] == "-fire":
			launchControl().control("-f", 2)
		if sys.argv[1] == "-s" or sys.argv[1] == "-stop":
			launchControl().controlContin("-s")
