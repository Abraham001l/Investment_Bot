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
invested = False
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
    invested = model.predict(inputs)[0] == 1

    # Terminating Scheduler To Move On
    scheduled_id.remove()
    scheduler.shutdown(wait=False)

daily_times = [7, 1, 2, 3, 4]

def schedule_daily():
    today = datetime.now()
    if today.day not in daily_times or today.hour >= 20:
        today = today+timedelta(days=1)
    today.hour, today.minute, today.second = 20, 0, 0
    scheduler = BlockingScheduler()
    scheduled_id = scheduler.add_job(run_model, 'date', run_date=today)

# ---------- Setting Up Functions For Hourly Runs ----------
def run_investment_algorithm():

    None

hourly_times = [[8,31], [9,31], [10, 31], [11, 31], [12, 31], [13, 31], [14, 31]] # [Hour, Minute]

def schedule_hourly():
    today = datetime.now()
    today.hour, today.minute, today.second = 20, 0, 0

# ---------- Live Run Loop ----------
while True:
    if not invested:
        schedule_daily()
        scheduler.start()
    else:
        None