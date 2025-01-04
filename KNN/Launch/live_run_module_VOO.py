import schedule
import time
import pytz
from datetime import datetime

def job():
    print('ran')

central_tz = pytz.timezone('US/Central')
schedule.every().day.at("10:45", central_tz).do(job)

while True:
    schedule.run_pending()
    time.sleep(10)
    print(datetime.now())