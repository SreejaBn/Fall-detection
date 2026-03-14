import network
import time
import gc
import machine
from imu import MPU6050
from machine import Pin, I2C
import math

# ---------- WIFI SETUP ----------
ssid = "TECNO POVA 4"
password = "i guess ok"

wlan = network.WLAN(network.STA_IF)
wlan.active(True)

print("Connecting to WiFi...")

wlan.connect(ssid, password)

attempt = 0
while not wlan.isconnected() and attempt < 10:
    attempt += 1
    print("Attempt", attempt)
    time.sleep(1)

if wlan.isconnected():
    print("Connected!")
    print("IP Address:", wlan.ifconfig()[0])
else:
    print("WiFi connection FAILED")

# ---------- SENSOR SETUP ----------
LED = Pin("LED", Pin.OUT)

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
imu = MPU6050(i2c)

free_fall_threshold = 0.5

counter = 0

while True:

    ax = imu.accel.x
    ay = imu.accel.y
    az = imu.accel.z

    gx = imu.gyro.x
    gy = imu.gyro.y
    gz = imu.gyro.z

    temp = imu.temperature

    # total acceleration magnitude
    A = math.sqrt(ax*ax + ay*ay + az*az)

    # free fall detection
    if A < free_fall_threshold:
        print("FREE FALL DETECTED!", round(A,2))
        LED.on()
    else:
        LED.off()

    # print every 5 cycles (reduces memory load)
    counter += 1
    if counter >= 5:
        print("ACC:", round(A,2),
              "GYRO:", round(math.sqrt(gx*gx+gy*gy+gz*gz),2),
              "TEMP:", round(temp,2))
        counter = 0

    # force memory cleanup
    gc.collect()

    time.sleep(0.05)
