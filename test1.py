import time
import board
import busio
from adafruit_pm25.i2c import PM25_I2C
from adafruit_lsm6ds.lsm6dsox import LSM6DSOX
from tabulate import tabulate

# Initialize I2C buses for sensors
i2c_lsm_1 = board.I2C()
i2c_lsm_2 = board.I2C()
i2c_lsm_3 = board.I2C()
i2c_pm = busio.I2C(board.SCL, board.SDA, frequency=100000)

# Create instances of LSM6DSOX for each sensor
sensor_1 = LSM6DSOX(i2c_lsm_1)
sensor_2 = LSM6DSOX(i2c_lsm_2)
sensor_3 = LSM6DSOX(i2c_lsm_3)

# Create instance of PM2.5 sensor
pm25 = PM25_I2C(i2c_pm, None)

print("Sensors initialized, reading data...")

# Open a text file for LSM6DSOX sensor data
with open("lsm_sensor_data.txt", "w") as lsm_file:
    # Open a text file for PM2.5 sensor data
    with open("pm25_sensor_data.txt", "w") as pm25_file:
        while True:
            try:
                # Read data from LSM6DSOX sensor 1
                acceleration_1 = sensor_1.acceleration
                gyro_1 = sensor_1.gyro

                # Read data from LSM6DSOX sensor 2
                acceleration_2 = sensor_2.acceleration
                gyro_2 = sensor_2.gyro

                # Read data from LSM6DSOX sensor 3
                acceleration_3 = sensor_3.acceleration
                gyro_3 = sensor_3.gyro

                # Format LSM6DSOX sensor data into table
                lsm_table = [
                    ["Sensor", "Acceleration (m/s^2)", "Gyro (radians)"],
                    ["1", acceleration_1, gyro_1],
                    ["2", acceleration_2, gyro_2],
                    ["3", acceleration_3, gyro_3]
                ]

                # Write formatted LSM6DSOX sensor table to the file
                lsm_file.write("LSM6DSOX Sensor Data:\n")
                lsm_file.write(tabulate(lsm_table, headers="firstrow"))
                lsm_file.write("\n\n")

                # Read data from PM2.5 sensor
                pm_data = pm25.read()

                # Format PM2.5 sensor data into table
                pm_table = [
                    ["Concentration Units", "Standard", "Environmental"],
                    ["PM 1.0", pm_data["pm10 standard"], pm_data["pm10 env"]],
                    ["PM 2.5", pm_data["pm25 standard"], pm_data["pm25 env"]],
                    ["PM 10", pm_data["pm100 standard"], pm_data["pm100 env"]],
                    ["Particles > 0.3um / 0.1L air", pm_data["particles 03um"], ""],
                    ["Particles > 0.5um / 0.1L air", pm_data["particles 05um"], ""],
                    ["Particles > 1.0um / 0.1L air", pm_data["particles 10um"], ""],
                    ["Particles > 2.5um / 0.1L air", pm_data["particles 25um"], ""],
                    ["Particles > 5.0um / 0.1L air", pm_data["particles 50um"], ""],
                    ["Particles > 10 um / 0.1L air", pm_data["particles 100um"], ""],
                ]

                # Write formatted PM2.5 sensor table to the file
                pm25_file.write("PM2.5 Sensor Data:\n")
                pm25_file.write(tabulate(pm_table, headers="firstrow"))
                pm25_file.write("\n\n")

            except RuntimeError as error:
                print(f"Error: {error}")
                print("Retrying...")
                continue

            # Add a delay between readings
            time.sleep(0.5)

print("Data saved to lsm_sensor_data.txt and pm25_sensor_data.txt")
