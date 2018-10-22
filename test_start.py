import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setup(23,gpio.OUT)

gpio.output(23,gpio.HIGH)
time.sleep(6)
gpio.cleanup()
