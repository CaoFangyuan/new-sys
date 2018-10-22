import RPi.GPIO as gpio
import os, sys
import readdata6
import time

gpio.setmode(gpio.BCM)
gpio.setup(21,gpio.IN)
gpio.setup(22,gpio.IN)
flag = 1
button1_counter = 0
button2_counter = 0
try:
    while flag == 1:
        button1 = gpio.input(21)
        button2 = gpio.input(22)
        if button2 == 0:
            button2_counter = button2_counter + 1
        else:
            button2_counter = 0
        if button2_counter >= 20:
            button2_counter = 0
            print("stop")
            os.system("shutdown -t now")   
            sys.exit()
        if button1 == 0:
            button1_counter = button1_counter + 1
        else:
            button1_counter = 0
        if button1_counter >= 20:
            button1_counter = 0
            print("begin")
            readdata6.main()
            print("finish")
            time.sleep(10)
except KeyboardInterrupt:
    gpio.cleanup()
finally:
    gpio.cleanup()
