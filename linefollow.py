'''
*Team Id: 5728
*Author List: Shaswat Singh, Sindhiya Arya, Shivank Bali, Pratik Joshi
'Filename: planterbot.py
*Theme: Planter Bot
*Functions: motor
*Global Variables: 
'''


import cv2
import numpy as np
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import RPi.GPIO as GPIO


'''
*Class Name : PWM_object
*Input: Pins Numbers for Enable, IN 1, IN 2 and inital frequency of the PWM cycle
*Ouput: Provides an easy interface to handle motors and LEDs
*Logic: Collection of common commands for PWM objects
'''

class PWM_object(object):
	
	# initialise the class
	# E_PIN = Enable PIN
	# A_PIN = IN 1 PIN
	# B_PIN = IN 2 PIN

	def __init__(self, E_PIN, freq):
		
		self.E  =   E_PIN
		self.freq = freq		

		# creates a PWM on the Enable PIN
		self.PWM  = GPIO.PWM(self.E,self.freq)

	def set_extrapins(A_PIN, B_PIN):
		
		# to be used for motors
		self.A = A_PIN
		self.B = B_PIN
	
	def clockwise(self):
		
		# configures the motors to turn in clockwise direction	
		GPIO.output(self.A, GPIO.HIGH)
		GPIO.output(self.B, GPIO.LOW)
	
	def counter_clockwise(self):
		
		# configures the motors to turn in counter-clockwise direction
		GPIO.output(self.A, GPIO.LOW)
		GPIO.output(self.B, GPIO.HIGH)

	
	def start(self):
		
		# starts the object at 0% power
		self.PWM.start(0)
	
	def stop(self):
		
		# stops the object
		self.PWM.stop()
	
	def change_cycle(self, cycle):

		# changes the duty cycle (% of power recieved) of the object
		self.PWM.ChangeDutyCycle(cycle)

	
'''
*Function Name: motor
*Input: left,right -> the pins controllling the left and right motors
	steer -> the direction into which the bot has to steer
*Output: calculates the speed of different motors according to the steer variable
	 changes the duty cycle of the motors according to these speeds
*Logic: if steer = 0, go straight
	if steer > 0, go right
	if steer < 0, go left
*Example Call: motor(left,right,45)
'''

def motor(left, right, steer):
	
	# these are the speeds in which the bot runs straight
	# these speeds are found by experimenting with the bot
	l_speed = l_speed_const 
	r_speed = r_speed_const	
	
	# configuring the motors to turn in clockwise direction
	left.clockwise()
	right.clockwise()

	# calculating speeds
	if (steer == 0):
		# if steer = 0 go straight
		pass
	elif (steer > 0):
		# if steer > 0 go right
		steer = 100 - steer
		l_speed = l_speed*steer/100 
	else:
		# if steer < 0 go left
		# making steer positive so as to calculate speed
		steer = steer*-1
	
		steer = 100 - steer
		r_speed = r_speed*steer/100 		
	
	# configuring to turn in counter-clockwise direction
	if r_speed < 0:
		right.counter_clockwise()
		rspeed = rspeed *-1
	if l_speed < 0:
		left.counter_clockwise()
		l_speed = lspeed * -1
	
	# Changing the duty cycle of the motors
	right.change_cycle(r_speed)
	left.change_cycle(l_speed)


		
'''
*Function Name: main
*Input: None
*Output: linefollow.avi showing the path detection by the bot
*Logic: read the comments before each section
*Example Call: called automatically when the file is executed
'''


# initilize the Raspberry PI GPIO

GPIO.setwarnings(True)
	
GPIO.setmode(GPIO.BOARD)

######### MOTOR CONFIGURATION #######################

#----------DEFINE MOTOR DRIVER PINS--------------

# Motor A, Right Side GPIO Constants 
PWM_DRIVE_RIGHT    = 37 # ENA - H-Bridge enable Pair
FORWARD_RIGHT_PIN  = 33 # IN1 - Forward Drive
BACKWARD_RIGHT_PIN = 35 # IN2 - Backward Drive

# Motor B, Left Side GPIO Constants
PWM_DRIVE_LEFT     = 40 # ENB - H-Bridge enable Pair
FORWARD_LEFT_PIN   = 36 # IN3 - Forward Drive
BACKWARD_LEFT_PIN  = 38 # IN4 - Backward Drive
#--------------------------------------------------


# setup of Motor Pins
GPIO.setup(FORWARD_RIGHT_PIN,  GPIO.OUT)
GPIO.setup(BACKWARD_RIGHT_PIN, GPIO.OUT)
GPIO.setup(PWM_DRIVE_RIGHT,    GPIO.OUT)

GPIO.setup(FORWARD_LEFT_PIN,   GPIO.OUT)
GPIO.setup(BACKWARD_LEFT_PIN,  GPIO.OUT)
GPIO.setup(PWM_DRIVE_LEFT,     GPIO.OUT)


# Setting Enable Pins To HIGH
GPIO.output(PWM_DRIVE_RIGHT,   GPIO.HIGH)
GPIO.output(PWM_DRIVE_LEFT,    GPIO.HIGH)

# variable declaration for motors
right = PWM_Object(PMW_DRIVE_RIGHT, 100)
right.set_extrapins(FORWARD_RIGHT_PIN, BACKWARD_RIGHT_PIN)
left  = PWM_Object(PWM_DRIVE_LEFT,  100)
left.set_extrapins(FORWARD_LEFT_PIN, BACKWARD_LEFT_PIN)

# configuring motors to run in clockwise direction 
right.clockwise()
left.clockwise()

# starting motor at 0% power
left.start()
right.start()

###########################################################

################## LED CONFIGURATION ######################

#----------DEFINE LED PINS--------------
RED_LED_PIN   = pin_number
BLUE_LED_PIN  = pin_number
GREEN_LED_PIN = pin_number
#----------------------------------------

# setup of LED Pins
GPIO.setup(RED_LED_PIN,   GPIO.OUT)
GPIO.setup(BLUE_LED_PIN,  GPIO.OUT)
GPIO.setup(GREEN_LED_PIN, GPIO.OUT)

# seting LED Pins HIGH
GPIO.setup(RED_LED_PIN,   GPIO.HIGH)
GPIO.setup(BLUE_LED_PIN,  GPIO.HIGH)
GPIO.setup(GREEN_LED_PIN, GPIO.HIGH)

# Making PWM Objects with 1s delay
red_led   = PWM_object(RED_LED_PIN,   1)
blue_led  = PWM_object(BLUE_LED_PIN,  1)
green_led = PWM_object(GREEN_LED_PIN, 1)

# Shutting Down LEDs
red_led.start()
blue_led.start()
green_led.start()

##########################################################

# codec initialization and declaring output video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('linefollow.avi',fourcc, 15, (640,480))


#---------------PICAM Initialization------------
camera = PiCamera()
camera.resolution = (320, 240)
camera.framerate = 15
rawCapture = PiRGBArray(camera,(320, 240))
#------------------------------------------------

# ERROR CONSTANTS
kp = 0.4	# error from midpoint constant
ap = 0.5	# angular deviation constant


for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True,splitter_port=2,resize=(320,240)):		
	# getting camera ready
	time.sleep(0.5)
	
	# obtaining image from the camera
	image = frame.array	
	
	# variables constants for black color range
	lb = np.array([0,0,0])
	ub = np.array([75,75,75])
	
	# obtaining an image with only black color	
	Blackline = cv2.inRange(image, lb, ub)	
	
	# kernel for eroding and dilating
	kernel = np.ones((3,3), np.uint8)
	
	# removing noise using the opening operation
	Blackline = cv2.morphologyEx(Blackline, cv2.MORPH_OPEN, kernel)
	
	# finding contours for the path
	img_blk,contours_blk, hierarchy_blk = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	# finding the angle of the path	
	blackbox = cv2.minAreaRect(contours_blk[0])
	(x_min, y_min), (w_min, h_min), ang = blackbox

	if ang < -45 :

		ang = 90 + ang

	if w_min < h_min and ang > 0:	  

		ang = (90-ang)*-1

	if w_min > h_min and ang < 0:

		ang = 90 + ang	  

	# midpoint of the screen
	setpoint = 160
	
	# deviation of the path from the center of the screen
	error = int(x_min - setpoint) 
	
	# angular deviation of the path
	ang = int(ang)	 

	# running the motor
	motor(left,right, (error*kp) + (ap*ang))
	
	# plotting the rectangle on the screen
	box = cv2.boxPoints(blackbox)

	box = np.int0(box)

	cv2.drawContours(image,[box],0,(0,0,255),3)	 

	# writing angular deviation to the image
	cv2.putText(image,str(ang),(10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

	# writing deviation from the center to the image
	cv2.putText(image,str(error),(10, 440), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

	# plotting a line at the center of the minimum area rectangle
	cv2.line(image, (int(x_min),0 ), (int(x_min),480 ), (255,0,0),3)

	# writing the image to the output	
	out.write(image)

	# clearing the input buffer
	rawCapture.truncate(0)	

	# condition to terminate in between
	key = cv2.waitKey(1) & 0xFF	
	
	if key == ord("q"):
		break

# clearing output buffer
out.release()

# stopping PWMs
left.stop()
right.stop()
red_led.stop()
blue_led.stop()
green_led.stop()

# stopping signal to PWMs
GPIO.output(PWM_DRIVE_RIGHT, GPIO.LOW)
GPIO.output(PWM_DRIVE_LEFT,  GPIO.LOW)
GPIO.output(RED_LED_PIN,     GPIO.LOW)
GPIO.output(BLUE_LED_PIN,    GPIO.LOW)
GPIO.output(GREEN_LED_PIN,   GPIO.LOW)

# garbage collection
GPIO.cleanup()
