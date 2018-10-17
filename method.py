class Sensor_data():
    def __init__(self):
        self.package = 0
        self.acceleration = Acceleration()
        self.gyroscope = Gyroscope()
        self.magnetometer = Magnetometer()
        self.quaternion = Quaternion()

class Acceleration():
    def __init__(self):
        self.acc_x = 0
        self.acc_y = 0
        self.acc_z = 0
class Gyroscope():
    def __init__(self):
        self.gyro_x = 0
        self.gyro_y = 0
        self.gyro_z = 0
class Magnetometer():
    def __init__(self):
        self.mag_x = 0
        self.mag_y = 0
        self.mag_z = 0
class Quaternion():
    def __init__(self):
        self.qua1 = 0
        self.qua2 = 0
        self.qua3 = 0
        self.qua4 = 0

class Sensor():
    def __init__(self):
        self.sensor_data = Sensor_data()

