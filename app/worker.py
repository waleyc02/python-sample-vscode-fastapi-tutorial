# app/worker.py

from app.scheduler import start_scheduler
import time

start_scheduler()

print("Worker started successfully")

while True:
    time.sleep(60)