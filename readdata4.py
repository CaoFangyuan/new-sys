#coding=utf-8
import spidev
import time 
import numpy as np
import RPi.GPIO as gpio
import sys
from method import *
import calculatesensor
import fpa
import testi2c

def BytesToHex(Bytes):
    return ''.join(["0x%02X " % x for x in Bytes]).strip()

if __name__ == "__main__":
    # Set motors
    testi2c.motor(0)
    testi2c.motor(2)
    testi2c.motor(3)
    gpio.setmode(gpio.BCM)
    gpio.setup(21,gpio.IN)
    rawdata = []
    # set spi
    spi = spidev.SpiDev()
    spi.open(0,0)
    spi.max_speed_hz = 15600000 
    spi.mode = 0b00
    spi.xfer2([0x81,0x08])
    spi.xfer2([0x88,0x20])
    spi.xfer2([0x89,0x80])
    spi.xfer2([0x8B,0x03])
    spi.xfer2([0x90,0xFF])
    spi.xfer2([0x9C,0x02])
    spi.xfer2([0x9E,0x0A])
    time.sleep(1)
    #IRQ = gpio.input(29)
    data = []
    head_index = 1
    first_flag = 1
    i = 0
    real_data = []
    acceleration = Acceleration()
    gyroscope = Gyroscope()
    magnetometer = Magnetometer()
    quaternion = Quaternion()
    sensor_data = Sensor_data()
    sensor1 = Sensor()
    #print(IRQ)
    # First read register 
    resp = spi.xfer2([0x01,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    print(BytesToHex(resp))
    #IRQ = gpio.input(29)
    #print(IRQ)
    # Second read register to clear over flow error of rx
    resp = spi.xfer2([0x01,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    print(BytesToHex(resp))
    try:
        # read data
        pac128 = [0x00,0,0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        resp1 = spi.xfer2(pac128)
        print(BytesToHex(resp1))
        number = spi.xfer2([0x12,0])
        print(number)
        while True:
            if number[1] == 74:
                pac74 = [0x00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                resp2 = spi.xfer2(pac74)
                #print(BytesToHex(resp2))
                number = spi.xfer2([0x12,0])
                if first_flag == 1:
                    #print(0)
                    while i <=74:
                        i = i+1
                        if i>=3:
                            if (resp2[i] == 54) and (resp2[i-1] == 255) and (resp2[i-2] == 250):
                                head_index = i-2
                                #print(head_index)
                                i = i-2
                                break
                    first_flag = 2
                    while i<=74: 
                        data.append(resp2[i])
                        i = i+1
                elif first_flag == 2:
                    i = 1
                    while i< head_index:
                        data.append(resp2[i])
                        i = i + 1
                    #print(data)
                    real_data = data[4:-1]
                    print(real_data)
                    real_data = bytearray(real_data)
                    #print(real_data)
                    sensor1 = calculatesensor.calsensor(real_data,sensor1)
                    #(angle, step) = fpa.fpa(sensor1)
                    #print(angle)
                    #print(step)
                    print(sensor1.sensor_data.acceleration.acc_z)
                    if sensor1.sensor_data.acceleration.acc_z>10:
                        testi2c.motor_control(0,1)
                    elif sensor1.sensor_data.acceleration.acc_z < 0:
                        testi2c.motor_control(2,1)
                    else:
                        testi2c.motor_control(0,0)
                        testi2c.motor_control(2,0)
                    print("_________________________________________")
                    data = []
                    real_data = []
                    i = head_index
                    while i<=74:
                        data.append(resp2[i])
                        i = i+1
                #print(data)
                #data = []
            else:
                while number[1] < 74:
                    number = spi.xfer2([0x12,0])
                    #print(number)
    except KeyboardInterrupt:
        spi.close()
        gpio.cleanup()
        print("finish")
