import requests
import schedule
import time
def run_job():
    output = requests.get("http://127.0.0.1:5000/api/trig_cron_send")
    print("git got")

schedule.every(30).seconds.do(run_job)

while True:
    schedule.run_pending()
    time.sleep(1)