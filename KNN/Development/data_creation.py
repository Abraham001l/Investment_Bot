import yfinance as yf
import pandas as pd
import numpy as np
import os

# ---------- Setting Up Directory ----------
cur_dir = os.getcwd()

# ---------- Basic Params ----------
ticker = 'VOO'
start_date = '2020-01-01'
end_date = '2024-01-05' # 2023-11-14
data_filename = 'VOO_2020-01-01_2023-11-24.csv'
data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)

# ---------- Getting Stock Data ----------
data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=False)
data.reset_index(inplace=True)
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

# Adding Breakout Labels
data.loc[:, 'Breakout'] = data['Adj Close'].shift(-5) >= (data['Adj Close'] * 1.01)
data.loc[:, 'Breakout'] = data['Breakout'].astype(bool).astype(int)
data.dropna()

data.to_csv(data_filename, index=False)