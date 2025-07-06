import random
import csv
from datetime import datetime, timedelta

def generate_data():
    with open('data/battery_log.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'soc', 'voltage'])
        for i in range(100):
            timestamp = (datetime.now() - timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S')
            soc = random.randint(10, 100)  # Simulate battery %
            voltage = round(3.0 + (soc / 100 * 1.5), 2)  # Fake voltage
            writer.writerow([timestamp, soc, voltage])

if __name__ == "__main__":
    generate_data()
