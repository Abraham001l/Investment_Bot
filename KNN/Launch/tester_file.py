# from data_collection_module import update_dataset
# import os
# import pandas as pd

# cur_dir = os.getcwd()

# data_filename = 'VOO_all.csv'
# data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)

# update_dataset('VOO')
# data = pd.read_csv(data_filename)
# print(data.iloc[-1])

import yfinance as yf
import pytz
from datetime import datetime

x = datetime.now()
print(x.strftime('%Y-%m-%d'))

central_tz = pytz.timezone('US/Central')
data = yf.download('VOO', start=x.strftime('%Y-%m-%d'), interval='1m', auto_adjust=False)
data.index = data.index.tz_convert(central_tz)
print(data)
print(data['Adj Close'])

# from apscheduler.schedulers.background import BlockingScheduler
# from datetime import datetime, timedelta

# def job2():
#     # print(scheduler.state)
#     print('executed')

# def job():
#     print('ran')
#     job2()
#     scheduler.shutdown(wait=False)

# while True:
#     global scheduler
#     scheduler = BlockingScheduler()
#     scheduled_id = scheduler.add_job(job, 'date', run_date=(datetime.now()+timedelta(seconds=5)))
#     print('back')
#     scheduler.start()
#     print('im here')
# print(datetime.now())



# from datetime import datetime, timedelta

# x = datetime.now()
# y = x
# y = y.replace(hour=20, minute=0, second=0, microsecond=0)+timedelta(days=1)
# print(y)
# print(x.minute)
# print(x.isoweekday())

# import pandas as pd
# import os

# cur_dir = os.getcwd()
# data_filename = os.path.join(cur_dir, 'KNN\\Launch\\InvestmentTrackers', 'investment_history.csv')
# df = pd.read_csv(data_filename)
# new_row = pd.DataFrame({'Date':[4], 'Adj Close':[23]})
# df = pd.concat([df, new_row],ignore_index=True)
# df.to_csv(data_filename, index=False)

# from datetime import datetime

# print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))

# from dotenv import load_dotenv, dotenv_values
# from email.message import EmailMessage
# import ssl
# import smtplib
# import os

# load_dotenv()

# email_sender = os.getenv("EMAIL")
# email_password = os.getenv("APP_PASSWORD")
# email_receiver = os.getenv("EMAIL")

# em = EmailMessage()
# em['From'] = email_sender
# em['To'] = email_receiver
# em['Subject'] = 'subject'
# em.set_content('body')

# context = ssl.create_default_context()

# with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
#     smtp.login(email_sender, email_password)
#     smtp.sendmail(email_sender, email_receiver, em.as_string())