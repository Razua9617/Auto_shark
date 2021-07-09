#!/usr/bin/python3
# CODE FOR AUTO SHARK

#import time


def colored(r, g, b, tevaluet):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, tevaluet)


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

# Greet Function | DONE
def greet():
	print("\nWelcome to AutoShark")

# This function will only print the menu | DONE
def menu():
		print("""\nPlease select from the following options:
	1-Extract ips and form a count
	2-images, smtp, binary files
	3-errors
	4-indicators of compromise
	5-All the above
	""")

# Use this function to prompt a user to ask what option they want to choose
def get_choice():
	# Use this list for validaton
	option = ['1','2','3','4','5']

	while True:
		choice = input("Choice: ")
		# Once we get the input from the user, we use isnumeric() function to confirm if the input is a number string or alpha string
		if choice.isnumeric():
			# if it is a number string, then we run this code
			if choice in option:
				return choice
			else:
				print("YOU BROKE IT\n")
				continue
			# otherwise, run this code
		else:
			print("YOU BROKE IT\n")
			continue

# Use this function to prompt the user if they wna tot use the program again
def prompt_again():
	# Ask user for there input if they wanna try again
	answer = input("\nWould you like to do something else (Y/N): ")
	return answer.lower()

# Simple function to say Goodbye
def bye():
	print("\nGoodbye")

# This function is just to loop through the different options
def loop():
	# the value variable will call the get_choice() function, and store the choice in the value variable.
	while True:
		# calling the menu() function here to print the menu()
		menu()
		# calling the get_choice() function here to get the user input and store it into a 'value' variable
		value = get_choice()
		if value == '1':
			print("You chose to extract ips and get a count") 
			#extractip()
			# prompt the user to see if they would like to do something else
			prompt = prompt_again()
			if prompt == 'y':
				continue
			else:
				bye()
				break
			
			#x = done(start)
		elif value == '2':
			print("You chose to extract image, smtp,and binary files") 
			#files()
			# prompt the user to see if they would like to do something else
			prompt = prompt_again()
			if prompt == 'y':
				continue
			else:
				bye()
				break
			
		elif value == '3':
			print("You chose to extract any error messages")
			#errors()
			# prompt the user to see if they would like to do something else
			prompt = prompt_again()
			if prompt == 'y':
				continue
			else:
				bye()
				break
			
		elif value == '4':
			print("You chose to extract any Indicators of Compromise(IOC)")
			#ioc()
			# prompt the user to see if they would like to do something else
			prompt = prompt_again()
			if prompt == 'y':
				continue
			else:
				bye()
				break
			
		elif value == '5':
			print("You chose option 5")
			#all()
			# prompt the user to see if they would like to do something else
			prompt = prompt_again()
			if prompt == 'y':
				continue
			else:
				bye()
				break

intro()
greet()
loop()


## we call intro(), greet(), then loop()
#time.sleep(5) #We can turn this on when we finish the program


