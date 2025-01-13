import pytz
from datetime import datetime, timedelta
import os
import pickle
import pandas as pd
from apscheduler.schedulers.background import BlockingScheduler
import yfinance as yf
from dotenv import load_dotenv, dotenv_values
from email.message import EmailMessage
import ssl
import smtplib
import numpy as np

# ---------- Setting Up Directory & Env Variable ----------
cur_dir = os.getcwd()
load_dotenv()

# ---------- Basic Params ----------
ticker = 'VOO'
prcnt_gain = .01
data_filename = 'VOO_all.csv'
model_filename = 'VOO_2020-10-15_2023-12-29.pkl'
data_filename = os.path.join(cur_dir, 'KNN\\Launch\\Datasets', data_filename)
model_filename = os.path.join(cur_dir, 'KNN\\Launch\\Models', model_filename)
history_filename = os.path.join(cur_dir, 'KNN\\Launch\\InvestmentTrackers', 'trade_tracker.csv')

# ---------- Important Global Variables ----------
investing = False
scheduler = None
central_tz = pytz.timezone('US/Central')
entry_price = None

# ---------- Function For Gathering Data For Model Execution ----------
def update_dataset():
    # ---------- Basic Params ----------
    data_filename = f'{ticker}_all.csv'
    data_filename = os.path.join(cur_dir, 'KNN\\Launch\\Datasets', data_filename)

    # ---------- Getting Stock Data ----------
    data = yf.download(ticker, start='2020-01-01', auto_adjust=False)
    data.reset_index(inplace=True)
    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')  # Convert Date to strings
    data.columns = data.columns.get_level_values(0) # Removes multi-header structure

    # ---------- Creating Features ----------
    data['Return'] = data['Adj Close'].pct_change()
    data.dropna()

    # MACD (Percentage)
    ema_12 = data['Adj Close'].ewm(span=12, adjust=False).mean()
    ema_26 = data['Adj Close'].ewm(span=26, adjust=False).mean()
    data.loc[:, 'MACD (%)'] = 100 * (ema_12 - ema_26) / ema_12

    # Percentage distance from 200-day MA
    ma_200 = data['Adj Close'].rolling(window=200).mean()
    data.loc[:, '% Distance 200MA'] = 100 * (data['Adj Close'] - ma_200) / ma_200

    # Volume Ratio
    data.loc[:, 'Volume Ratio'] = data['Volume'] / data['Volume'].rolling(window=20).mean()

    # ATR
    data.loc[:, 'ATR'] = data['High'].rolling(window=14).max() - data['Low'].rolling(window=14).min()

    # RSI
    data.loc[:, 'RSI'] = 100 - (100 / (1 + (data['Return'].rolling(window=14).mean() / data['Return'].rolling(window=14).std())))

    # Volatility (Standard Deviation of Returns over a 20-day window)
    data.loc[:, 'Volatility'] = data['Return'].rolling(window=20).std() * np.sqrt(252)  # Annualized volatility
    
    # Drop rows with NaN values created by rolling calculations
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)

    # ---------- Exporting Data ----------
    data.to_csv(data_filename, index=False)

# ---------- Alert Function ----------
def send_alert(subject, body):
    email_sender = os.getenv("EMAIL")
    email_password = os.getenv("APP_PASSWORD")
    email_receiver = os.getenv("EMAIL")

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())

# ---------- Setting Up Functions For Daily Runs ----------
def mark_entry(stock_data):
    trade_history = pd.read_csv(history_filename)
    blank_row = pd.DataFrame({'Date':[0], 'Adj Close':[0]})
    entry_price = stock_data.iloc[-1]['Adj Close']
    entry_row = pd.DataFrame({'Date':[datetime.now().strftime("%m/%d/%Y, %H:%M:%S")],
                              'Adj Close':entry_price})
    trade_history = pd.concat([trade_history, blank_row],ignore_index=True)
    trade_history = pd.concat([trade_history, entry_row],ignore_index=True)
    trade_history.to_csv(history_filename, index=False)

def run_model():
    # Updating VOO_all.csv & Reading In Data
    update_dataset()
    daily_data = pd.read_csv(data_filename)

    # Running Model
    model = pickle.load(open(model_filename, 'rb'))
    inputs = pd.DataFrame([daily_data.iloc[-1][['MACD (%)', '% Distance 200MA', 'Volume Ratio', 'ATR', 'RSI', 'Volatility']]])
    global investing
    investing = model.predict(inputs)[0] == 1
    if investing:
        mark_entry(daily_data)
        send_alert(f"ENTERED VOO {daily_data.iloc[-1]['Adj Close']}", "TRADED")

    # Terminating Scheduler To Move On
    global scheduler
    scheduler.shutdown(wait=False)

daily_times = [7, 1, 2, 3, 4]

def schedule_daily():
    today = datetime.now()
    if today.isoweekday() not in daily_times or (today.hour >= 20 and today.second >= 1):
        today = today+timedelta(days=1)
    exec_date = today.replace(hour=20, minute=0, second=0, microsecond=0)
    global scheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(run_model, 'date', run_date=exec_date)
    print(f'Scheduled Model Execution For {exec_date}')

# ---------- Setting Up Algorithm Functions ----------
def stop_loss_algo(cur_price): # Works On Any Timeframe Data
    global investing

    # Stop Loss Algo
    if cur_price <= entry_price*(1-prcnt_gain/2):
        investing = False
        send_alert(f"EXITED VOO {cur_price}", "TRADED")

def momentum_algo(cur_price, last_price): # Works On Hourly Data
    global investing

    # Momentum Algo
    expected_prcnt_gain = ((prcnt_gain/5)/7)*.5
    last_prcnt_gain = last_price/entry_price
    cur_prcnt_gain = cur_price/entry_price
    if cur_prcnt_gain-last_prcnt_gain < expected_prcnt_gain and investing:
        investing = False
        send_alert(f"EXITED VOO {cur_price}", "TRADED")

# ---------- Setting Up Functions For Hourly Runs ----------
def run_investment_algorithm():
    # Opening History and Minute Data
    trade_history = pd.read_csv(history_filename)
    minute_data = yf.download('VOO', start='2025-01-06', interval='1m')
    minute_data.columns = minute_data.columns.get_level_values(0) # Removes multi-header structure

    # Gathering Values For Calculations
    last_price = trade_history.iloc[-1]['Adj Close']
    hour_price = minute_data.iloc[-2]['Adj Close']

    stop_loss_algo(hour_price)
    
    momentum_algo(hour_price, last_price)
    
    # Updating Trade History
    new_log = pd.DataFrame({'Date':[datetime.now().strftime("%m/%d/%Y, %H:%M:%S")],
                              'Adj Close':hour_price,
                              'LogTimeFrame':'Hourly'})
    trade_history = pd.concat([trade_history, new_log],ignore_index=True)
    trade_history.to_csv(history_filename, index=False)

    # Terminating Scheduler To Move On
    global scheduler
    scheduler.shutdown(wait=False)

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
    scheduler = BlockingScheduler()
    scheduler.add_job(run_investment_algorithm, 'date', run_date=exec_date)
    print(f'Scheduled Algorithm Check For {exec_date}')

# ---------- Setting Up Functions For Minutely Runs ----------
def run_minute_stop_loss():
    # Opening History and Minute Data
    trade_history = pd.read_csv(history_filename)
    minute_data = yf.download('VOO', start='2025-01-06', interval='1m')
    minute_data.columns = minute_data.columns.get_level_values(0) # Removes multi-header structure

    # Gathering Values For Calculations
    hour_price = minute_data.iloc[-2]['Adj Close']

    stop_loss_algo(hour_price)

    # Updating Trade History
    new_log = pd.DataFrame({'Date':[datetime.now().strftime("%m/%d/%Y, %H:%M:%S")],
                              'Adj Close':hour_price,
                              'LogTimeFrame':'Minutely'})
    trade_history = pd.concat([trade_history, new_log],ignore_index=True)
    trade_history.to_csv(history_filename, index=False)

    # Terminating Scheduler To Move On
    global investing
    global scheduler
    if not investing:
        scheduler.shutdown(wait=False)
    else:
        schedule_minutely()

def schedule_minutely():
    today = datetime.now()
    td_time = today.hour+(today.minute/60)
    if td_time >= 8.5 and td_time <= 14.75:
        exec_date = today+timedelta(minutes=10)
        global scheduler
        scheduler.add_job(run_minute_stop_loss, 'date', run_date=exec_date)


# ---------- Live Run Loop ----------
while True:
    if not investing:
        schedule_daily()
        scheduler.start()
    else:
        schedule_hourly()
        schedule_minutely()
        scheduler.start()