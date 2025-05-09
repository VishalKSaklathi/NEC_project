import time
import datetime
from DFRobot_MICS import DFRobot_MICS_I2C

# Define gas type constants
CO = 0x01
CH4 = 0x02
C2H5OH = 0x03
H2 = 0x06
NH3 = 0x08
NO2 = 0x0A

# Initialize sensor
I2C_BUS = 1  # I2C bus number (usually 1 on Raspberry Pi)
mics = DFRobot_MICS_I2C(I2C_BUS, 0x75)  # Replace 0x75 with your sensor's I2C address if different
print("I2C device found successfully\n")

def main():
    # Wake up the sensor if it's in sleep mode
    if mics.get_power_mode() == 0x00:  # SLEEP_MODE
        mics.wakeup_mode()
        print("Sensor woke up from sleep mode.")
    else:
        print("Sensor is already in wakeup mode.")

    # Warm-up and calibration
    print("Warming up sensor...Wait for 3 minutes...")
    mics.warm_up_time(3)  # 3-minute warm-up

    print("Starting gas readings...")

    while True:
        # Get current timestamp
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Read gas concentrations
        co = mics.get_gas_ppm(CO)
        ch4 = mics.get_gas_ppm(CH4)
        nh3 = mics.get_gas_ppm(NH3)
        ethanol = mics.get_gas_ppm(C2H5OH)
        no2 = mics.get_gas_ppm(NO2)
        h2 = mics.get_gas_ppm(H2)

        # Display readings with timestamp
        print(f"Timestamp: {now}")
        print(f"CO     : {co:.2f} ppm")
        print(f"CH4    : {ch4:.2f} ppm")
        print(f"NH3    : {nh3:.2f} ppm")
        print(f"Ethanol: {ethanol:.2f} ppm")
        print(f"NO2    : {no2:.2f} ppm")
        print(f"H2     : {h2:.2f} ppm")

        # Safety warnings
        warnings = []
        if co > 400:
            warnings.append("CO levels are above safe limits!")
        if ethanol > 200:
            warnings.append("Alcohol exceeding 200 ppm!")
        if nh3 > 25:
            warnings.append("NH3 levels are above safe levels!")

        if warnings:
            for warning in warnings:
                print(warning)
        else:
            print("All gases are within safe limits.")

        print("-" * 40)
        time.sleep(2)

if __name__ == "__main__":
    main()
#x
