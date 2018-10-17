import RPi.GPIO as gpio
import readdata5

gpio.setmode(gpio.BCM)
gpio.setup(21,gpio.IN)
flag = 1
button1_counter = 0
try:
    while flag == 1:
        button1 = gpio.input(21)
        if button1 == 0:
            button1_counter = button_counter + 1
        else:
            button1_counter = 0
        if button1_counter >= 20:
            button1_counter = 0
            readdata5.main()
except KeyboardInterrupt:
    gpio.cleanup()
