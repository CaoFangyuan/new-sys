import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(7,gpio.OUT)
gpio.output(7, gpio.HIGH)
time.sleep(5)
gpio.output(7,gpio.LOW)
time.sleep(2)
gpio.output(7,gpio.HIGH)
gpio.cleanup()

