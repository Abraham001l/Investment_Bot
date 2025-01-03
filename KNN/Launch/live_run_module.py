import schedule
import time
import pytz
from datetime import datetime

def job():
    print('ran')

central_tz = pytz.timezone('US/Central')
schedule.every().day.at("14:31", central_tz).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
    print(datetime.now())