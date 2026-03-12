import machine
from imu import MPU6050
from machine import Pin, I2C
import time
import math

LED = machine.Pin("LED", machine.Pin.OUT)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

def read_sensor():

    ax = imu.accel.x
    ay = imu.accel.y
    az = imu.accel.z

    gx = imu.gyro.x
    gy = imu.gyro.y
    gz = imu.gyro.z

    temp = imu.temperature

    return ax, ay, az, gx, gy, gz, temp


def compute_motion(ax, ay, az, gx, gy, gz):

    acc_mag = math.sqrt(ax*ax + ay*ay + az*az)

    gyro_mag = math.sqrt(gx*gx + gy*gy + gz*gz)

    tilt = math.degrees(math.atan2(ax, math.sqrt(ay*ay + az*az)))

    return acc_mag, gyro_mag, tilt


while True:

    ax, ay, az, gx, gy, gz, temp = read_sensor()

    acc_mag, gyro_mag, tilt = compute_motion(ax, ay, az, gx, gy, gz)

    print(
        "ACC:", round(acc_mag,2),
        "GYRO:", round(gyro_mag,2),
        "TILT:", round(tilt,2),
        "TEMP:", round(temp,2)
    )

    time.sleep(0.02)   # 50Hz sampling
