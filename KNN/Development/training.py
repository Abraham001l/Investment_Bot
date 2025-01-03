import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import pickle
import os

# ---------- Setting Up Directory ----------
cur_dir = os.getcwd()

# ---------- Basic Params ----------
data_filename = 'VOO_2020-01-01_2023-11-24.csv'
model_filename = 'VOO_2020-01-01_2023-11-24.pkl'
data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)
model_filename = os.path.join(cur_dir, 'KNN\\Development\\Models', model_filename)

# ---------- Preparing Features and Labels ----------
data = pd.read_csv(data_filename)
features = data[['MACD (%)', '% Distance 200MA', 'Volume Ratio', 'ATR', 'RSI', 'Volatility']]
labels = data['Breakout']

# ---------- Training KNN Model ----------
k = 3
knn = KNeighborsClassifier(n_neighbors=k)
knn.fit(features, labels)

# ---------- Saving KNN Model ----------
with open(model_filename, 'wb') as file:
    pickle.dump(model_filename, file)
print(f"Model saved to {model_filename}")