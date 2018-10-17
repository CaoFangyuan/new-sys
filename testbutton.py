import RPi.GPIO as gpio

gpio.setmode(gpio.BCM)
gpio.setup(21,gpio.IN)
gpio.setup(22,gpio.IN)

initial_flag = 1
b = 0
try:
    while initial_flag == 1:
        a = gpio.input(21)
        if a == 0:
            b = b+1
except KeyboardInterrupt:
    gpio.cleanup()
    print(b)
    print("finish")
