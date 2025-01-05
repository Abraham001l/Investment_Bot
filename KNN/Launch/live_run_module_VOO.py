import pytz
from datetime import datetime
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
data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)
model_filename = os.path.join(cur_dir, 'KNN\\Development\\Models', model_filename)

# ---------- Important Global Variables ----------
invested = False
scheduler = BlockingScheduler()
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

# ---------- Setting Up Functions For Hourly Runs ----------
def run_investment_algorithm():
    None

# ---------- Live Run Loop ----------
