import pickle
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import os
import pytz

# ---------- Setting Up Directory ----------
cur_dir = os.getcwd()

# ---------- Basic Params ----------
ticker = 'VOO'
prcnt_gain = .01
data_filename = 'VOO_2024-01-02_2024-12-06.csv'
model_filename = 'VOO_2020-10-15_2023-12-29.pkl' #VOO_2020-10-15_2024-06-28.pkl
data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)
model_filename = os.path.join(cur_dir, 'KNN\\Development\\Models', model_filename)
central_tz = pytz.timezone('US/Central')

# ---------- Seting Up Model ----------
model = pickle.load(open(model_filename, 'rb'))
data = pd.read_csv(data_filename)

# ---------- Simulation Loop ----------
balance = 100
balances = []
invested = False
entry_price = None
entry_i = None
days_invested = 0

for i in range(len(data)-1):
    if not invested:
        print(days_invested)
        # Running Model
        inputs = pd.DataFrame([data.iloc[i][['MACD (%)', '% Distance 200MA', 'Volume Ratio', 'ATR', 'RSI', 'Volatility']]])
        prediction = model.predict(inputs)[0]

        # Processing Response
        invested = prediction == 1
        entry_price = data.iloc[i]['Close']
        entry_i = i
        days_invested = 1
    else:
        # Retrieving Hourly Data
        hourly_data = yf.download(ticker, start=data.iloc[i]['Date'], end=data.iloc[i+1]['Date'], auto_adjust=False, interval='1h')
        if not hourly_data.empty:
            hourly_data.columns = hourly_data.columns.get_level_values(0) # Removes multi-header structure
            hourly_data.index = hourly_data.index.tz_convert(central_tz)
            # Looping Through Hourly Data
            if days_invested == 1:
                # entry_price = hourly_data.iloc[0]['Adj Close']
                # print(days_invested)
                # print(hourly_data.iloc[0])
                last_price = entry_price
            for i in range(len(hourly_data)):
                hour_price = hourly_data.iloc[i]['Close']

                # Stop Loss Algo
                if hour_price <= entry_price*(1-prcnt_gain/2):
                    invested = False
                    balance *= (hour_price/entry_price)
                    break
                
                # Momentum Algo
                expected_prcnt_gain = ((prcnt_gain/5)/7)*.5
                last_prcnt_gain = last_price/entry_price
                cur_prcnt_gain = hour_price/entry_price
                if cur_prcnt_gain-last_prcnt_gain < expected_prcnt_gain:
                    invested = False
                    balance *= (hour_price/entry_price)
                    break
                last_price = hour_price
        days_invested += 1
    # Updating Balacne
    balances.append(balance)
data['Balance'] = balances+[balance]

# ---------- Plotting Simulation ----------
plt.figure(figsize=(12, 6))
plt.plot(data['Date'], data['Balance'], label='Portfolio Balance')
plt.xlabel('Date')
plt.ylabel('Balance ($)')
# plt.title(f'Investment Strategy Performance on {ticker} {test_data.iloc[-1]['Balance']}')
plt.legend()
plt.show()