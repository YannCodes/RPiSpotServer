#!/usr/bin/env python
# -*- coding: utf-8 -*-

#RPiSpotServer
#Copyright (C) 2015 Yann Lochet
#
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket
from time import sleep
try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script")

#init GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#TCP constants
HOST=""
PORT=12345
ADDR=(HOST,PORT)
BUFSIZE=4096
MAXQCON=5

#socket creation
serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(ADDR)
serv.listen(MAXQCON)

#GPIO setup
GPIO.setup(1, GPIO.OUT)
GPIO.setup(2, GPIO.OUT)
GPIO.setup(3, GPIO.OUT)

try :
    while 1:

      print("listening...")
      client, cli_addr = serv.accept()
      print("connected to %s at %s" % (client,cli_addr))

      data = client.recv(BUFSIZE)
      print "\"" + data + "\""
    
      if data[1:3] == "on":
	print("compliant text ! => turning on LED")
	GPIO.output(int(data[0]), GPIO.HIGH)
       
      if data[1:3] == "of":
	print("compliant text ! => turning off LED")
	GPIO.output(int(data[0]), GPIO.LOW)

      client.close()
	
except KeyboardInterrupt:
    print("\ninterrupt received, proceeding…") 
    serv.close()
    quit()
