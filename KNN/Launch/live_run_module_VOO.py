import schedule
import time
import pytz
from datetime import datetime
import os
from KNN.Launch.data_collection_module import update_dataset
import pickle
import pandas as pd

# ---------- Setting Up Directory ----------
cur_dir = os.getcwd()

# ---------- Basic Params ----------
ticker = 'VOO'
data_filename = 'VOO_all.csv'
model_filename = 'VOO_2020-10-15_2023-12-29.pkl'
data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)
model_filename = os.path.join(cur_dir, 'KNN\\Development\\Models', model_filename)

# ---------- Setting Up Functions ----------
def run_model():
    # Updating VOO_all.csv & Reading In Data
    update_dataset(ticker)
    data = pd.read_csv(data_filename)

    # Running Model
    model = pickle.load(open(model_filename, 'rb'))
    inputs = pd.DataFrame([data.iloc[-1][['MACD (%)', '% Distance 200MA', 'Volume Ratio', 'ATR', 'RSI', 'Volatility']]])
    prediction = model.predict(inputs)[0]
    None

central_tz = pytz.timezone('US/Central')
schedule.every().sunday.at("20:00", central_tz).do(run_model)
schedule.every().monday.at("20:00", central_tz).do(run_model)
schedule.every().tuesday.at("20:00", central_tz).do(run_model)
schedule.every().wednesday.at("20:00", central_tz).do(run_model)
schedule.every().thursday.at("20:00", central_tz).do(run_model)


# ---------- Live Run Loop ----------
invested = False
while True:
    if invested:
        None
    else:

    None


central_tz = pytz.timezone('US/Central')
schedule.every().day.at("10:45", central_tz).do(job)

while True:
    if invested: