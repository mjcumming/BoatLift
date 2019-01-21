"""This program uses an MPU6050 to determine x/y inclination with smoothing using Kalman

from https://github.com/rocheparadox/Kalman-Filter-Python-for-mpu6050

"""


from mpu6050 import mpu6050

from Kalman import KalmanAngle

import time

import math

i2c_bus = 1
device_address = 0x68
radToDeg = 57.2957786

class Inclinometer:

    RestrictPitch = True 

    kalmanX = KalmanAngle()
    kalmanY = KalmanAngle()
    
    gyroXAngle = None
    gyroYAngle = None
    
    compAngleX = None
    compAngleY = None

    kalAngleX = 0
    kalAngleY = 0

    timer = None

    def __init__(self, address = device_address,bus = i2c_bus):
        self.mpu = mpu6050 (address,bus)

        time.sleep (1)

        accel = self.mpu.get_accel_rawdata ()
        #print (accel)

        if self.RestrictPitch:
            roll = math.atan2(accel["y"],accel["z"]) * radToDeg
            pitch = math.atan(-accel["x"]/math.sqrt((accel["y"]**2)+(accel["z"]**2))) * radToDeg
        else:
            roll = math.atan(accel["y"]/math.sqrt((accel["x"]**2)+(accel["z"]**2))) * radToDeg
            pitch = math.atan2(-accel["x"],accel["z"]) * radToDeg

        self.kalmanX.setAngle(roll)
        self.kalmanY.setAngle(pitch)
        
        self.gyroXAngle = roll
        self.gyroYAngle = pitch
        self.compAngleX = roll
        self.compAngleY = pitch

        self.timer = time.time()

    def get_angles (self):
        #Read Accelerometer raw value
        accel = self.mpu.get_accel_rawdata ()

        #Read Gyroscope raw value
        gyro = self.mpu.get_gyro_rawdata()

        dt = time.time() - self.timer
        self.timer = time.time()

        roll = 0
        pitch = 0

        if (self.RestrictPitch):
            roll = math.atan2(accel["y"],accel["z"]) * radToDeg
            pitch = math.atan(-accel["x"]/math.sqrt((accel["y"]**2)+(accel["z"]**2))) * radToDeg
        else:
            roll = math.atan(accel["y"]/math.sqrt((accel["x"]**2)+(accel["z"]**2))) * radToDeg
            pitch = math.atan2(-accel["x"],accel["z"]) * radToDeg

        gyroXRate = gyro["x"]/131
        gyroYRate = gyro["y"]/131

        if (self.RestrictPitch):

            if((roll < -90 and self.kalAngleX >90) or (roll > 90 and self.kalAngleX < -90)):
                self.kalmanX.setAngle(roll)
                self.complAngleX = roll
                self.kalAngleX   = roll
                self.gyroXAngle  = roll
            else:
                self.kalAngleX = self.kalmanX.getAngle(roll,gyroXRate,dt)

            if(abs(self.kalAngleX)>90):
                gyroYRate  = -gyroYRate
                self.kalAngleY  = self.kalmanY.getAngle(pitch,gyroYRate,dt)
        else:

            if((pitch < -90 and self.kalAngleY >90) or (pitch > 90 and self.kalAngleY < -90)):
                self.kalmanY.setAngle(pitch)
                self.complAngleY = pitch
                self.kalAngleY   = pitch
                self.gyroYAngle  = pitch
            else:
                self.kalAngleY = self.kalmanY.getAngle(pitch,gyroYRate,dt)

            if(abs(self.kalAngleY)>90):
                gyroXRate  = -gyroXRate
                self.kalAngleX = self.kalmanX.getAngle(roll,gyroXRate,dt)

        self.gyroXAngle = gyroXRate * dt
        self.gyroYAngle = self.gyroYAngle * dt # ?? error

        self.compAngleX = 0.93 * (self.compAngleX + gyroXRate * dt) + 0.07 * roll
        self.compAngleY = 0.93 * (self.compAngleY + gyroYRate * dt) + 0.07 * pitch

        if ((self.gyroXAngle < -180) or (self.gyroXAngle > 180)):
            self.gyroXAngle = self.kalAngleX
        if ((self.gyroYAngle < -180) or (self.gyroYAngle > 180)):
            self.gyroYAngle = self.kalAngleY

        #print("Angle X: " + str(self.kalAngleX)+"   " +"Angle Y: " + str(self.kalAngleY))
        return int(self.kalAngleX),int(self.kalAngleY)
                     
if __name__ == "__main__":
    inc = Inclinometer()
 

    while True:
        x,y = inc.get_angles()
        print("Angle X: " + str(int (x))+"   " +"Angle Y: " + str(int(y)))
        time.sleep (1)
