#!/usr/bin/python
# Import required Python libraries
import RPi.GPIO as GPIO
import time
from subprocess import call

GPIO.setmode(GPIO.BOARD)
GPIO_PIR = 23
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

Current_State  = 0
Previous_State = 0

try:

  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0

  # Loop until users quits with CTRL-C
  while True :

    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)

    if Current_State==1 and Previous_State==0:
      # PIR is triggered
      call(['curl', 'http://127.0.0.1:7999/1/config/set?emulate_motion=on'])
      # Record previous state
      Previous_State=1
    elif Current_State==0 and Previous_State==1:
      # PIR has returned to ready state
      call(['curl', 'http://127.0.0.1:7999/1/config/set?emulate_motion=off'])
      Previous_State=0

    # Wait for 10 milliseconds
    time.sleep(0.01)

except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()
