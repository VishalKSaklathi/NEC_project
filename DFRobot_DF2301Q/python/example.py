import sys
import time

# Add DFRobot library path (update if needed)
sys.path.append('./DFRobot_DF2301Q')

from DFRobot_MICS import DFRobot_MICS_I2C

# I2C address for MICS-4514 (ADDRESS_3 = 0x78)
I2C_ADDRESS = 0x75
CALIBRATION_TIME = 3  # in minutes

# Initialize sensor
mics = DFRobot_MICS_I2C(i2c_addr=I2C_ADDRESS, bus=1)

def setup():
    print("Initializing sensor...")
    while not mics.begin():
        print("Sensor not detected. Retrying...")
        time.sleep(1)
    print("Sensor connected!")

    # Wake up the sensor if it's sleeping
    if mics.get_power_state() == mics.SLEEP_MODE:
        mics.wake_up_mode()
        print("Sensor woke up.")
    else:
        print("Sensor already awake.")

    # Warm-up time for calibration
    print(f"Calibrating for {CALIBRATION_TIME} minutes...")
    while not mics.warm_up_time(CALIBRATION_TIME):
        print("Warming up... Please wait.")
        time.sleep(1)
    print("Calibration complete.")

def loop():
    try:
        while True:
            # Read all gases
            ethanol = mics.get_gas_data(mics.C2H5OH)
            co      = mics.get_gas_data(mics.CO)
            no2     = mics.get_gas_data(mics.NO2)
            nh3     = mics.get_gas_data(mics.NH3)
            h2      = mics.get_gas_data(mics.H2)
            ch4     = mics.get_gas_data(mics.CH4)

            # Print results
            print(f"Ethanol (C2H5OH): {ethanol:.1f} PPM")
            print(f"Carbon Monoxide (CO): {co:.1f} PPM")
            print(f"Nitrogen Dioxide (NO2): {no2:.2f} PPM")
            print(f"Ammonia (NH3): {nh3:.1f} PPM")
            print(f"Hydrogen (H2): {h2:.1f} PPM")
            print(f"Methane (CH4): {ch4:.1f} PPM")
            print("-------------------------------")

            time.sleep(2)

    except KeyboardInterrupt:
        print("Program stopped.")

if __name__ == '__main__':
    setup()
    loop()
