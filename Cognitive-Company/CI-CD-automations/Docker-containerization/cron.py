import os
import time

def run_cron():
    print("Centaurion cron started")
    schedule = os.environ.get('SCHEDULE', 'not configured')
    print(f"Schedule: {schedule}")
    
    while True:
        time.sleep(60)

if __name__ == "__main__":
    run_cron()
