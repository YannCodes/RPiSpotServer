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
for pin in range(1,7):
    GPIO.setup(pin, GPIO.OUT)

state=GPIO.HIGH
pin=-1

try :
    while 1:

        print("listening...")
        client, cli_addr = serv.accept()
        print("connected to %s at %s" % (client,cli_addr))

        data = client.recv(BUFSIZE)
        print "\"" + data + "\""
        
        if data[0:2] == "on":
            state=GPIO.HIGH
        if data[0:2] == "of":
            state=GPIO.LOW
            
        color = data[2:5]
        print(color)
        if color == "Bl1":
            pin=1
        if color == "Bl2":
            pin=2
        if color == "Gre":
            pin=3
        if color == "Yel":
            pin=4
        if color == "Ora":
            pin=5
        if color ==  "Red":
            pin=6
        
        if pin != -1:
            GPIO.output(pin, state)
            print("state : %s %s" % (pin,state))

        if color == "All":
            for pin in range(1,7):
                GPIO.output(pin, state)
                print("state : %s %s" % (pin,state))

        client.close()
        pin=-1
	
except KeyboardInterrupt:
    print("\ninterrupt received, proceeding…") 
    serv.close()
    quit()
