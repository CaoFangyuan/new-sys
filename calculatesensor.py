import struct
def calsensor(data,sensor):
    '''sensor.sensor_data.pakage=data[3:5]
    sensor.sensor_data.pakage,=struct.unpack('!h',sensor.sensor_data.pakage)
    sensor.sensor_data.pakage =int(sensor.sensor_data.pakage)'''
    
    sensor.sensor_data.quaternion.qua1=data[8:12]
    sensor.sensor_data.quaternion.qua1,=struct.unpack('!f',sensor.sensor_data.quaternion.qua1)
    sensor.sensor_data.quaternion.qua2=data[12:16]
    sensor.sensor_data.quaternion.qua2,=struct.unpack('!f',sensor.sensor_data.quaternion.qua2)
    sensor.sensor_data.quaternion.qua3=data[16:20]
    sensor.sensor_data.quaternion.qua3,=struct.unpack('!f',sensor.sensor_data.quaternion.qua3) 
    sensor.sensor_data.quaternion.qua4=data[20:24]
    sensor.sensor_data.quaternion.qua4,=struct.unpack('!f',sensor.sensor_data.quaternion.qua4)

    sensor.sensor_data.acceleration.acc_x=data[27:31]
    sensor.sensor_data.acceleration.acc_x,=struct.unpack('!f',sensor.sensor_data.acceleration.acc_x)
    sensor.sensor_data.acceleration.acc_y=data[31:35]
    sensor.sensor_data.acceleration.acc_y,=struct.unpack('!f',sensor.sensor_data.acceleration.acc_y)
    sensor.sensor_data.acceleration.acc_z=data[35:39]
    sensor.sensor_data.acceleration.acc_z,=struct.unpack('!f',sensor.sensor_data.acceleration.acc_z)

    sensor.sensor_data.gyroscope.gyro_x=data[42:46]
    sensor.sensor_data.gyroscope.gyro_x,=struct.unpack('!f',sensor.sensor_data.gyroscope.gyro_x)
    sensor.sensor_data.gyroscope.gyro_y=data[46:50]
    sensor.sensor_data.gyroscope.gyro_y,=struct.unpack('!f',sensor.sensor_data.gyroscope.gyro_y)
    sensor.sensor_data.gyroscope.gyro_z=data[50:54]
    sensor.sensor_data.gyroscope.gyro_z,=struct.unpack('!f', sensor.sensor_data.gyroscope.gyro_z)

    sensor.sensor_data.magnetometer.mag_x=data[57:61]
    sensor.sensor_data.magnetometer.mag_x,=struct.unpack('!f', sensor.sensor_data.magnetometer.mag_x)
    sensor.sensor_data.magnetometer.mag_y=data[61:65]
    sensor.sensor_data.magnetometer.mag_y,=struct.unpack('!f', sensor.sensor_data.magnetometer.mag_y)
    sensor.sensor_data.magnetometer.mag_z=data[65:]
    sensor.sensor_data.magnetometer.mag_z,=struct.unpack('!f', sensor.sensor_data.magnetometer.mag_z)

    return sensor

