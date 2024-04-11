import time
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25.i2c import PM25_I2C
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX

# Set up PM2.5 sensor
reset_pin = None
i2c_pm = busio.I2C(board.SCL, board.SDA, frequency=100000)
pm25 = PM25_I2C(i2c_pm, reset_pin)

# Set up LSM6DSOX sensor
i2c_lsm = board.I2C()
sensor = LSM6DSOX(i2c_lsm)

print("Sensors initialized, reading data...")

while True:
    time.sleep(1)

    # Read PM2.5 sensor data
    try:
        aqdata = pm25.read()
    except RuntimeError:
        print("Unable to read from PM2.5 sensor, retrying...")
        continue

    print("\nPM2.5 Sensor Data:")
    print("------------------------")
    print("Concentration Units (standard)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 standard"], aqdata["pm25 standard"], aqdata["pm100 standard"])
    )
    print("Concentration Units (environmental)")
    print("---------------------------------------")
    print(
        "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
        % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
    )
    print("---------------------------------------")
    print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
    print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
    print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
    print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
    print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
    print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
    print("---------------------------------------")

    # Read LSM6DSOX sensor data
    print("\nLSM6DSOX Sensor Data:")
    print("------------------------")
    print("Acceleration: X: %.2f, Y: %.2f, Z: %.2f m/s^2" % sensor.acceleration)
    print("Gyro: X: %.2f, Y: %.2f, Z: %.2f radians" % sensor.gyro)
    print("------------------------")
