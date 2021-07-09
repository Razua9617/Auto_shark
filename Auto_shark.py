#!/usr/bin/python3
# CODE FOR AUTO SHARK

import time
import sys
import pyshark
import re
import dpkt
import socket

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def intro():
  print(colored(255, 0, 0,"""
         .8.       8 8888      88 8888888 8888888888 ,o888888o.       d888888o.   8 8888        8          .8.          8 888888888o.   8 8888     ,88' 
        .888.      8 8888      88       8 8888    . 8888     `88.   .`8888:' `88. 8 8888        8         .888.         8 8888    `88.  8 8888    ,88'  
       :88888.     8 8888      88       8 8888   ,8 8888       `8b  8.`8888.   Y8 8 8888        8        :88888.        8 8888     `88  8 8888   ,88'   
      . `88888.    8 8888      88       8 8888   88 8888        `8b `8.`8888.     8 8888        8       . `88888.       8 8888     ,88  8 8888  ,88'    
     .8. `88888.   8 8888      88       8 8888   88 8888         88  `8.`8888.    8 8888        8      .8. `88888.      8 8888.   ,88'  8 8888 ,88'     
    .8`8. `88888.  8 8888      88       8 8888   88 8888         88   `8.`8888.   8 8888        8     .8`8. `88888.     8 888888888P'   8 8888 88'      
   .8' `8. `88888. 8 8888      88       8 8888   88 8888        ,8P    `8.`8888.  8 8888888888888    .8' `8. `88888.    8 8888`8b       8 888888<       
  .8'   `8. `88888.` 8888     ,8P       8 8888   `8 8888       ,8P 8b   `8.`8888. 8 8888        8   .8'   `8. `88888.   8 8888 `8b.     8 8888 `Y8.     
 .888888888. `88888. 8888   ,d8P        8 8888    ` 8888     ,88'  `8b.  ;8.`8888 8 8888        8  .888888888. `88888.  8 8888   `8b.   8 8888   `Y8.   
.8'       `8. `88888. `Y88888P'         8 8888       `8888888P'     `Y8888P ,88P' 8 8888        8 .8'       `8. `88888. 8 8888     `88. 8 8888     `Y8. """))

def options():
	choice = int(input("""
	Welcome to AutoShark 
	Please select from the following options:
	1-Extract ips and count
	2-images, smtp, binary files
	3-errors
	4-indicators of compromise
	5-All the above
	"""))
	return(choice)
def done(start):
	resp = input("Would you like to continue?(y/n)")
	if resp.lower == 'y' :
		break
	return()
def extractip():

def files():

def errors():

def ioc():

def all():
	extractip()
	files()
	errors()
	ioc()

intro()
#time.sleep(5) #We can turn this on when we finish the program
select = options()
pcap = sys.argv[1]

start = True
while(start):
	if select == 1:
		print("You choose option 1")
		extractip()
		start = False
		#start = done(start)
	elif select == 2:
		print("You choose option 2")
		files()
		start = False
		#start = done(start)
	elif select == 3:
		print("You choose option 3")
		errors()
		start = False
		#start = done(start)
	elif select == 4:
		print("You choose option 4")
		ioc()
		start = False
		#start = done(start)
	elif select == 5:
		print("You choose option 5")
		all()
		start = False
		#start = done(start)
	else:
		print("You selected a invalid option")
		start = False 
		#start = done(start)