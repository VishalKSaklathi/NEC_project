import Adafruit_DHT
import spidev
import time
import requests
import rpi.gpio
from datetime import datetime

# Constantsx
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 16  #xxx GPIO23
API_URL = "http://localhost:8000/api/upload"

# SPI Setup for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Read MCP3008 channel
def read_adc(channel):
    if 0 <= channel <= 7:
        adc = spi.xfer2([1, (8 + channel) << 4, 0])
        data = ((adc[1] & 3) << 8) + adc[2]
        return data * (3.3 / 1023.0)  # Convert to voltage (assuming 3.3V)
    return -1

# Warm-up phase for MiCS sensor (3xx minutes)
print("Warming up MiCS sensor for 3 minutes...")
start_time = time.time()
while time.time() - start_time < 30:
    for ch in range(6):
        _ = read_adc(ch)  # discard readings
    time.sleep(1)
print("Warm-up complete. Starting data collection...")

# Main loop
while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

    if humidity is not None and temperature is not None:
        sensor_data = {
            "DeviceId": "ABX2345JK",
            "DeviceStatus": "OK",
            "DeviceError": "0000.00",
            "uploadtimestamp": datetime.now().isoformat(),
            "DeviceRFId": "261AF283930334",
            "DeviceLatitude": "51.5669854",
            "DeviceLogitude": "0.2127605",
            "TimeSeriesDataPoints": [{
                "Countid": 1,
                "Timestamp": datetime.now().isoformat(),
                "humidity": humidity,
                "temperature": temperature,
                "CO": round(read_adc(0), 2),
                "NO2": round(read_adc(1), 2),
                "NH3": round(read_adc(2), 2),
                "H2": round(read_adc(3), 2),
                "CH4": round(read_adc(4), 2),
                "C2H5OH": round(read_adc(5), 2),
                "humidity-alarm": humidity > 80,
                "temperature-alarm": temperature > 40,
                "CO-alarm": False,
                "NO2-alrm": False,
                "NH3-alarm": None,
                "H2-alarm": False,
                "CH4-alarm": False,
                "C2H5OH-alarm": False
            }],
            "ModemInfo": {
                "IP": "192.168.0.101",
                "Networkimestamp": datetime.now().isoformat(),
                "RSSI": 2.10,
                "CellID": "123456",
                "UL": "10 mbps",
                "DL": "20 mbps",
                "MCC": "404",
                "MNC": "45",
                "STATUS": "OK"
            }
        }

        try:
            response = requests.post(API_URL, json=sensor_data)
            print("Uploaded:", response.status_code)
        except Exception as e:
            print("Upload failed:", e)

    else:
        print("Sensor read failed.")
    
    time.sleep(10)
