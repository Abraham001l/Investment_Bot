import yfinance as yf
import numpy as np
import os

# ---------- Setting Up Directory ----------
cur_dir = os.getcwd()

# ---------- Basic Params ----------
ticker = 'VOO'
all_true = False
prcnt_gain = .01
start_date = '2024-06-28'#2021-04-30
end_date = '2025-01-10' # 2024-06-28
data_filename = 'VOO_2024-06-28_2025-01-10.csv'
data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)

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

# Adding Breakout Labels
data.loc[:, 'Breakout'] = (data['Adj Close'].shift(-5) >= (data['Adj Close'] * (1+prcnt_gain))).astype(int)
data.dropna(inplace=True)
data.reset_index(drop=True, inplace=True)

# ---------- Cropping To Window Of Interest ----------
if not all_true:
    start_i = data.loc[data['Date'] == start_date].index[0]
    end_i = data.loc[data['Date'] == end_date].index[0]
    data = data.iloc[start_i:end_i+1]

# ---------- Exporting Data ----------
data.to_csv(data_filename, index=False)