from app.scheduler import start_scheduler
import time

start_scheduler()

while True:
    time.sleep(60)