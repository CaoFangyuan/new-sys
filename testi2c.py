import smbus
import RPi.GPIO as gpio
import time
#gpio.cleanup()
def setvoltagetime(rated_voltage, clamp_voltage):
    erm_cl_av_p = 21.18e-3
    erm_clamp_p = 21.64e-3
    idiss_time = 75e-6
    blanking_time = 75e-6
    drive_time = 3 *2e-3 + 1e-3
    rate = rated_voltage/erm_cl_av_p
    clamp = clamp_voltage*(drive_time+idiss_time+blanking_time)/erm_clamp_p/(drive_time-300e-6)
    return rate, clamp
def motor(num):
    if num ==0:
        en_num = 19
        trig_num = 7
        control = 0x01
    elif num ==1:
        en_num = 26
        trig_num = 12
        control = 0x02
    elif num ==2:
        en_num = 14
        trig_num = 16
        control = 0x04
    else:
        en_num = 15
        trig_num = 20
        control = 0x08
    channel = 1
    bus = smbus.SMBus(channel)
    gpio.setmode(gpio.BCM)
    # A1
    gpio.setup(17,gpio.OUT)
    # A2
    gpio.setup(27,gpio.OUT)
    #A3
    gpio.setup(18,gpio.OUT)
    #EN0
    gpio.setup(en_num,gpio.OUT)

    gpio.output(17,gpio.LOW)
    gpio.output(27,gpio.LOW)
    gpio.output(18,gpio.LOW)
    gpio.output(en_num,gpio.HIGH)

    gpio.setup(13,gpio.OUT)
    gpio.output(13,gpio.LOW)
    time.sleep(0.5)
    gpio.output(13,gpio.HIGH)
    bus.write_byte(0x70,control)
    time.sleep(0.05)
    bus.write_byte_data(0x5A,0x01,0x40)
    time.sleep(0.5)
    bus.write_byte_data(0x5A,0x1A,0x36)
    #bus.write_i2c_block_data(0xB4,resgister,data)
    #a = bus.read_byte_data(0x5A,0x1C)
    #rate, clamp = setvoltagetime(3.3,3.6)
    #print(rate)
    #print(clamp)
    bus.write_byte_data(0x5A,0x16,0x3D)
    bus.write_byte_data(0x5A,0x17,0XA7)
    bus.write_byte_data(0x5A,0x01,0x43)
    bus.write_byte_data(0x5A,0x1D,0x80)
    bus.write_byte_data(0x5A,0x01,0x03)
    c = bus.read_byte_data(0x5A,0x00)
    #print(c)
    #print(1)
def motor_control(num,state):
    if num ==0:
        trig_num = 7
    elif num ==1:
        trig_num = 12
    elif num ==2:
        trig_num = 16
    else:
        trig_num = 20
# 0 for stop and 1 for start
    gpio.setmode(gpio.BCM)
    gpio.setup(trig_num,gpio.OUT)
    if state ==1:
        gpio.output(trig_num,gpio.HIGH)
    elif state ==0:
        gpio.output(trig_num,gpio.LOW)
    #time.sleep(1)
    #gpio.cleanup()


#motor(0)
#start()
