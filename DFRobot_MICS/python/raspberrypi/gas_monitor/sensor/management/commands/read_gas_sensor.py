import time
import datetime
import json
import os
from django.core.management.base import BaseCommand
from DFRobot_MICS import DFRobot_MICS_I2C

# Define gas type constants
CO = 0x01
CH4 = 0x02
C2H5OH = 0x03
H2 = 0x06
NH3 = 0x08
NO2 = 0x0A

class Command(BaseCommand):
    help = 'Reads gas sensor data and stores it in a JSON file.'

    def handle(self, *args, **options):
        # Initialize sensor
        I2C_BUS = 1  # Adjust if necessary
        mics = DFRobot_MICS_I2C(I2C_BUS, 0x75)

        # Wake up the sensor if it's in sleep mode
        if mics.get_power_mode() == 0x00:  # SLEEP_MODE
            mics.wakeup_mode()
            self.stdout.write("Sensor woke up from sleep mode.")
        else:
            self.stdout.write("Sensor is already in wakeup mode.")

        # Warm-up and calibration
        self.stdout.write("Warming up sensor for 3 minutes...")
        mics.warm_up_time(3)  # 3-minute warm-up

        self.stdout.write("Starting gas readings...")

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

            # Prepare data dictionary
            data = {
                "timestamp": now,
                "CO_ppm": round(co, 2),
                "CH4_ppm": round(ch4, 2),
                "NH3_ppm": round(nh3, 2),
                "Ethanol_ppm": round(ethanol, 2),
                "NO2_ppm": round(no2, 2),
                "H2_ppm": round(h2, 2),
                "warnings": []
            }

            # Safety warnings
            if co > 400:
                data["warnings"].append("??  CO levels are above safe limits!")
            if ethanol > 200:
                data["warnings"].append("??  Alcohol exceeding 200 ppm!")
            if nh3 > 25:
                data["warnings"].append("??  NH3 levels are above safe levels!")
            if not data["warnings"]:
                data["warnings"].append("? All gases are within safe limits.")

            # Define file path
            base_dir = os.path.join('sensor_data')
            os.makedirs(base_dir, exist_ok=True)
            filename = f"gas_reading_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            file_path = os.path.join(base_dir, filename)

            # Write data to JSON file
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file, indent=4)

            self.stdout.write(f"Data written to {file_path}")
            time.sleep(2)
#x
