import RPi.GPIO as gpio
import os, sys

gpio.setmode(gpio.BCM)
gpio.setup(22,gpio.IN)
flag = 1
button2_counter = 0
try:
    while flag == 1:
        button1 = gpio.input(22)
        if button1 == 0:
            button2_counter = button2_counter + 1
        else:
            button2_counter = 0
        if button2_counter >= 20:
            button2_counter = 0
            print("stop")
            os.system("shutdown -t  now")   
            sys.exit()
except KeyboardInterrupt:
    gpio.cleanup()
finally:
    gpio.cleanup()
