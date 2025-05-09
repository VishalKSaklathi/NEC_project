import time
from DFRobot_MICS import DFRobot_MICS_I2C

I2C_BUS = 1
mics = DFRobot_MICS_I2C(I2C_BUS, 0x75)

def main():
    print("Waiting for sensor to become ready...")
    while not mics.check_data_ready():
        print("Sensor warming up...")
        time.sleep(1)

    print("Sensor ready. Reading gas concentrations...")

    while True:
        print(f"CO     : {mics.get_gas_data(mics.CO)} ppm")
        print(f"CH4    : {mics.get_gas_data(mics.CH4)} ppm")
        print(f"NH3    : {mics.get_gas_data(mics.NH3)} ppm")
        print(f"Ethanol: {mics.get_gas_data(mics.C2H5OH)} ppm")
        print(f"NO2    : {mics.get_gas_data(mics.NO2)} ppm")
        print(f"H2     : {mics.get_gas_data(mics.H2)} ppm")
        print("-" * 40)
        time.sleep(2)

if __name__ == "__main__":
    main()
