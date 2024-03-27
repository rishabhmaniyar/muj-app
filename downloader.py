import requests
import os
from datetime import datetime, timedelta
import time

def download_csv(url, folder):
    response = requests.get(url)
    if response.status_code == 200:
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        filename = f"{timestamp}.csv"
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {url} to {filepath}")
    else:
        print(f"Failed to download {url}")

# Main function to download CSV files for every 1 minute from 7:45AM to 8:30AM
def main():
    print("starting")
    start_time = datetime.now().replace(hour=7, minute=45, second=0, microsecond=0)
    end_time = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0)
    folder_equity = 'equity_csv'
    folder_series = 'series_change_csv'

    os.makedirs(folder_equity, exist_ok=True)
    os.makedirs(folder_series, exist_ok=True)

    while datetime.now() < end_time:
        if datetime.now() >= start_time:
            print("Time not found")
            download_csv('https://archives.nseindia.com/content/equities/EQUITY_L.csv', folder_equity)
            download_csv('https://archives.nseindia.com/content/equities/series_change.csv', folder_series)

        # Wait for 1 minute
        time.sleep(60)

if __name__ == "__main__":
    main()
