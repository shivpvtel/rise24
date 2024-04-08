import time
import board
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

i2c = board.I2C()
sensor = LSM6DSOX(i2c)

while True:
        print ("Acceleration: X/:%.2f, Y:%.2f, Z%.2f m/s^2" %(sensor.acceleration))
        print("Gyro: X/:%.2f, Y:%.2f, Z%.2f radians" % (sensor.gyro))
        print("")
        time.sleep(0.5)


