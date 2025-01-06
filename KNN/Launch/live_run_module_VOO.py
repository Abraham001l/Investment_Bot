import pytz
from datetime import datetime, timedelta
import os
from KNN.Launch.data_collection_module import update_dataset
import pickle
import pandas as pd
from apscheduler.schedulers.background import BlockingScheduler

# ---------- Setting Up Directory ----------
cur_dir = os.getcwd()

# ---------- Basic Params ----------
ticker = 'VOO'
data_filename = 'VOO_all.csv'
model_filename = 'VOO_2020-10-15_2023-12-29.pkl'
data_filename = os.path.join(cur_dir, 'KNN\\Launch\\Datasets', data_filename)
model_filename = os.path.join(cur_dir, 'KNN\\Launch\\Models', model_filename)

# ---------- Important Global Variables ----------
investing = False
scheduler = None
scheduled_id = None
central_tz = pytz.timezone('US/Central')

# ---------- Setting Up Functions For Daily Runs ----------
def run_model():
    # Updating VOO_all.csv & Reading In Data
    update_dataset(ticker)
    data = pd.read_csv(data_filename)

    # Running Model
    model = pickle.load(open(model_filename, 'rb'))
    inputs = pd.DataFrame([data.iloc[-1][['MACD (%)', '% Distance 200MA', 'Volume Ratio', 'ATR', 'RSI', 'Volatility']]])
    global investing
    investing = model.predict(inputs)[0] == 1

    # Terminating Scheduler To Move On
    global scheduler
    global scheduled_id
    scheduled_id.remove()
    scheduler.shutdown(wait=False)

daily_times = [7, 1, 2, 3, 4]

def schedule_daily():
    today = datetime.now()
    if today.isoweekday() not in daily_times or today.hour >= 20:
        today = today+timedelta(days=1)
    exec_date = today.replace(hour=20, minute=0, second=0, microsecond=0)
    global scheduler
    global scheduled_id
    scheduler = BlockingScheduler()
    scheduled_id = scheduler.add_job(run_model, 'date', run_date=exec_date)

# ---------- Setting Up Functions For Hourly Runs ----------
def run_investment_algorithm():
    
    None

hourly_times = [8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5] # [Hour, Minute]

def schedule_hourly():
    today = datetime.now()
    td_time = today.hour+(today.minute/60)
    time_location = 0
    day_delta = 0
    for i in range(len(hourly_times)):
        if td_time < hourly_times[i]:
            time_location = i
            day_delta = 0
            break
        if i == 6:
            time_location = 0
            day_delta = 1
    exec_date = today.replace(hour=int(hourly_times[time_location]), minute=30)+timedelta(days=day_delta)
    global scheduler
    global scheduled_id
    scheduler = BlockingScheduler()
    scheduled_id = scheduler.add_job(run_investment_algorithm, 'date', run_date=exec_date)


# ---------- Live Run Loop ----------
while True:
    if not investing:
        schedule_daily()
        scheduler.start()
    else:
        None