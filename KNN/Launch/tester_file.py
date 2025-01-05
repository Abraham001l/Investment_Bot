# from data_collection_module import update_dataset
# import os
# import pandas as pd

# cur_dir = os.getcwd()

# data_filename = 'VOO_all.csv'
# data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)

# update_dataset('VOO')
# data = pd.read_csv(data_filename)
# print(data.iloc[-1])

# import yfinance as yf
# import pytz

# central_tz = pytz.timezone('US/Central')
# data = yf.download('VOO', start='2025-01-03', interval='1h')
# data.index = data.index.tz_convert(central_tz)
# print(data)

from apscheduler.schedulers.background import BlockingScheduler

# def job():
#     print('ran')
#     scheduled_id.remove()
#     scheduler.shutdown(wait=False)

# scheduler = BlockingScheduler()
# scheduled_id = scheduler.add_job(job, 'interval', seconds = 3)

# while True:
#     scheduler.start()
#     print('im here')
#     scheduler = BlockingScheduler()
#     scheduled_id = scheduler.add_job(job, 'interval', seconds = 3)



# from datetime import datetime

# x = datetime.now()
# print(x.isoweekday())
