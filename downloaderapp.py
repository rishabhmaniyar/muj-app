from fastapi import FastAPI, BackgroundTasks
from datetime import datetime, timedelta
import requests
import os
import threading
import schedule
import time

app = FastAPI()

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

def schedule_task():
    # Schedule task to run at 7:45 AM every day
    schedule.every().day.at("07:45").do(download_csv, 'https://archives.nseindia.com/content/equities/EQUITY_L.csv', 'equity_csv')
    schedule.every().day.at("07:45").do(download_csv, 'https://archives.nseindia.com/content/equities/series_change.csv', 'series_change_csv')

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)  # Sleep for 60 seconds

@app.on_event("startup")
async def startup_event():
    # Start scheduler in a separate thread when the FastAPI app starts
    scheduler_thread = threading.Thread(target=run_scheduler)
    scheduler_thread.start()

@app.get("/")
async def read_root():
    return {"message": "Scheduled task to run at 7:45 AM every day"}
