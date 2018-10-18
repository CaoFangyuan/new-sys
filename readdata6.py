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
import csv
import fpa_parameter

def BytesToHex(Bytes):
    return ''.join(["0x%02X " % x for x in Bytes]).strip()

#if __name__ == "__main__":
def main():
    # Set motors
    print("begin")
    #Initial fpa_parameter
    fpa_parameter.step_count = 0
    fpa_parameter.fpalist = []
    fpa_parameter.stance = 0
    fpa_parameter.fpa_result = 0
    fpa_parameter.dt = 0.01
    fpa_parameter.zupt_state = 0
    fpa_parameter.zupt_count = 0
    fpa_parameter.flag_stance_to_swing = 0
    fpa_parameter.flag_swing_to_stance = 0
    fpa_parameter.stance_time = 0
    fpa_parameter.fpa_sum = 0
    fpa_parameter.velocity_world_x_old = 0
    fpa_parameter.velocity_world_y_old = 0
    fpa_parameter.velocity_world_z_old = 0
    fpa_parameter.position_world_x_old = 0
    fpa_parameter.position_world_y_old = 0
    fpa_parameter.position_world_z_old = 0
    fpa_parameter.position_world_x_lasttime = 0
    fpa_parameter.position_world_y_lasttime = 0
    fpa_parameter.position_world_z_lasttime = 0
    fpa_parameter.heading_vector_x_old = 0
    fpa_parameter.heading_vector_y_old = 0
    fpa_parameter.heading_vector_z_old = 0
    testi2c.motor(0)
    #testi2c.motor(2)
    #testi2c.motor(3)
    testi2c.motor_control(0,0)
    gpio.setmode(gpio.BCM)
    # button1
    gpio.setup(21,gpio.IN)

    csvfile = open("raw_data.csv",'w')
    writer = csv.writer(csvfile)
    writer.writerow(['package','qua0','qua1','qua2','qua3','angx','angy','angz'])
    csvfile = open("fpa.csv",'w')
    writer1 = csv.writer(csvfile)
    writer1.writerow(['fpa','step'])

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
    # state for training. Totoally has four
    state_flag = 0
    button1_counter = 0
    i = 0
    real_data = []
    acceleration = Acceleration()
    gyroscope = Gyroscope()
    magnetometer = Magnetometer()
    quaternion = Quaternion()
    sensor_data = Sensor_data()
    sensor1 = Sensor()
    baseline = []
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
        pac128 = [0x00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        resp1 = spi.xfer2(pac128)
        print(BytesToHex(resp1))
        number = spi.xfer2([0x12,0])
        print(number)
        while state_flag == 0:
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
                    print('____________________________________________')
                    #print(real_data)
                    sensor1 = calculatesensor.calsensor(real_data,sensor1)
                    #writer.writerow([sensor1.sensor_data.package,sensor1.sensor_data.quaternion.qua1,sensor1.sensor_data.quaternion.qua2,sensor1.sensor_data.quaternion.qua3,sensor1.sensor_data.quaternion.qua4,sensor1.sensor_data.gyroscope.gyro_x,sensor1.sensor_data.gyroscope.gyro_y,sensor1.sensor_data.gyroscope.gyro_z])
                    (angle, step) = fpa.fpa(sensor1)
                    if angle!=0:
                        baseline.append(angle)
                        writer1.writerow([angle,step])
                        fpa_parameter.fpa_result = 0
                    if step == 6:
                        base_fpa = (np.sum(baseline[1:]))/4
                        print("baseline_finish_____________________________________________________")
                        state_flag = 1
                    data = []
                    real_data = []
                    i = head_index
                    while i<=74:
                        data.append(resp2[i])
                        i = i+1
            else:
                while number[1] < 74:
                    number = spi.xfer2([0x12,0])
                    
        if state_flag == 1:
            data = []
            head_index = 1
            first_flag = 1
            i = 0
            real_data = []
            resp = spi.xfer2([0x01,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            print(BytesToHex(resp))
            resp = spi.xfer2([0x01,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
            print(BytesToHex(resp)) 
            pac128 = [0x00,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
            resp1 = spi.xfer2(pac128)
            print(BytesToHex(resp1))
            number = spi.xfer2([0x12,0])
            print(number)
            while state_flag == 1:
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
                        print('____________________________________________')
                        #print(real_data)
                        sensor1 = calculatesensor.calsensor(real_data,sensor1)
                        #writer.writerow([sensor1.sensor_data.package,sensor1.sensor_data.quaternion.qua1,sensor1.sensor_data.quaternion.qua2,sensor1.sensor_data.quaternion.qua3,sensor1.sensor_data.quaternion.qua4,sensor1.sensor_data.gyroscope.gyro_x,sensor1.sensor_data.gyroscope.gyro_y,sensor1.sensor_data.gyroscope.gyro_z])
                        (angle, step) = fpa.fpa(sensor1)
                        if angle!=0:
                            angle = base_fpa - angle
                            writer1.writerow([angle,step])
                            fpa_parameter.fpa_result = 0
                            if angle > 10:
                                testi2c.motor_control(0,1)
                            else:
                                testi2c.motor_control(0,0)
                        data = []
                        real_data = []
                        i = head_index
                        while i<=74:
                            data.append(resp2[i])
                            i = i+1
                else:
                    while number[1] < 74:
                        number = spi.xfer2([0x12,0])
                button1 = gpio.input(21)
                if button1 == 0:
                    button1_counter = button1_counter + 1
                else:
                    button1_counter = 0
                if button1_counter >= 20:
                    state_flag = 2
            if state_flag == 2:
                spi.close()
                csvfile.close()
                return 200
    except KeyboardInterrupt:
        spi.close()
        gpio.cleanup()
        csvfile.close()
        print("finish")
