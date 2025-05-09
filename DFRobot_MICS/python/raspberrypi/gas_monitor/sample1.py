import requests
import time
import datetime
import sys
import socket

#x Add path for sensor module
sys.path.append('/home/pi/~gas/DFRobot_MICS/python/raspberrypi')
from DFRobot_MICS import DFRobot_MICS_I2C

# Gas constants
CO = 0x01
CH4 = 0x02
C2H5OH = 0x03
H2 = 0x06
NH3 = 0x08
NO2 = 0x0A

# API endpointx (adjust this to your Django server IP and correct port)
API_ENDPOINT = "http://localhost:8000/api/gas/"  # e.g., http://192.168.1.100:8000/api/gas/

# Initialize sensorx
I2C_BUS = 1
mics = DFRobot_MICS_I2C(I2C_BUS, 0x75)

def initialize_sensor():
    if mics.get_power_mode() == 0x00:
        mics.wakeup_mode()
        print("Sensor woke up from sleep mode.")
    else:
        print("Sensor already in wakeup mode.")
    print("Warming up sensor for 3 minutes...")
    mics.warm_up_time(1)
    print("Sensor warm-up completed.")

def read_sensor():
    return {
        "timestamp": datetime.datetime.now().isoformat(),
        "co": round(mics.get_gas_ppm(CO), 2),
        "ch4": round(mics.get_gas_ppm(CH4), 2),
        "nh3": round(mics.get_gas_ppm(NH3), 2),
        "c2h5oh": round(mics.get_gas_ppm(C2H5OH), 2),
        "h2": round(mics.get_gas_ppm(H2), 2),
        "no2": round(mics.get_gas_ppm(NO2), 2),
        "humidity": 50.0,        # Use actual DHT11/DHT22 sensor if available
        "temperature": 28.5
    }

def prepare_payload(data):
    return {
        "timestamp": data["timestamp"],
        "humidity": data["humidity"],
        "temperature": data["temperature"],
        "CO": data["co"],
        "NO2": data["no2"],
        "NH3": data["nh3"],
        "H2": data["h2"],
        "CH4": data["ch4"],
        "C2H5OH": data["c2h5oh"],
        "humidity_alarm": data["humidity"] > 80,
        "temperature_alarm": data["temperature"] > 40,
        "CO_alarm": data["co"] > 10,
        "NO2_alarm": data["no2"] > 0.5,
        "H2_alarm": data["h2"] > 50,
        "CH4_alarm": data["ch4"] > 1000,
        "C2H5OH_alarm": data["c2h5oh"] > 100
    }

def main():
    initialize_sensor()

    while True:
        sensor_data = read_sensor()
        payload = prepare_payload(sensor_data)

        try:
            response = requests.post(API_ENDPOINT, json=payload)
            now = datetime.datetime.now().strftime("%H:%M:%S")
            if response.status_code == 201 or response.status_code == 200:
                print(f"[{now}] Upload successful.")
            else:
                print(f"[{now}] Failed upload: Status {response.status_code}")
                print("Response content:", response.text)
        except Exception as e:
            print(f"Exception during upload: {e}")

        time.sleep(10)

if __name__ == "__main__":
    main()
