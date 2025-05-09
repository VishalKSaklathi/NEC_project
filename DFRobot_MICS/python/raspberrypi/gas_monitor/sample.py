import requests
import time
import datetime
import json
import sys
sys.path.append('/home/pi/~gas/DFRobot_MICS/python/raspberrypi')
from DFRobot_MICS import DFRobot_MICS_I2C

#xxx Define gas type constantsx 
CO = 0x01
CH4 = 0x02
C2H5OH = 0x03
H2 = 0x06
NH3 = 0x08
NO2 = 0x0A

# Django API Endpoint x
API_ENDPOINT = "http://localhost:8000/api/gas/"  #x Replace with your Pi IP if needed

# Initialize sensor
I2C_BUS = 1  # I2C bus number (usually 1 on Raspberry Pi)
mics = DFRobot_MICS_I2C(I2C_BUS, 0x75)  # Replace 0x75 with your sensor's I2C address if different

# Wake up and warm up sensor
def initialize_sensor():
    if mics.get_power_mode() == 0x00:  # SLEEP_MODE
        mics.wakeup_mode()
        print("Sensor woke up from sleep mode.")
    else:
        print("Sensor already in wakeup mode.")

    print("Warming up sensor for 3 minutes...")
    mics.warm_up_time(1)  #x 3-minute warm-up
    print("Sensor warm-up completed.")

# Real sensor reading function
def read_sensor():
    # Read gas concentrations
    co = mics.get_gas_ppm(CO)
    ch4 = mics.get_gas_ppm(CH4)
    nh3 = mics.get_gas_ppm(NH3)
    ethanol = mics.get_gas_ppm(C2H5OH)
    no2 = mics.get_gas_ppm(NO2)
    h2 = mics.get_gas_ppm(H2)

    # Current timestamp
    now = datetime.datetime.now().isoformat()

    # Prepare data in Django API format
    data = {
        "timestamp": now,
        "co": round(co, 2),
        "no2": round(no2, 2),
        "nh3": round(nh3, 2),
        "h2": round(h2, 2),
        "ch4": round(ch4, 2),
        "c2h5oh": round(ethanol, 2)
    }

    return data

# Main loop to read and send data
def main():
    initialize_sensor()

    while True:
        sensor_data = read_sensor()

        try:
            response = requests.post(API_ENDPOINT, data=sensor_data)
            current_time = datetime.datetime.now().strftime("%H:%M:%S")
            if response.status_code == 201:
                print(f"[{current_time}] Data uploaded successfully: {sensor_data}")
            else:
                print(f"[{current_time}] Failed to upload: {response.status_code}")
        except Exception as e:
            print(f"Error uploading data: {e}")

        time.sleep(10)  # Send every 10 seconds

if __name__ == "__main__":
    main()
