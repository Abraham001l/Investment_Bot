import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import pickle
import os

# ---------- Setting Up Directory ----------
cur_dir = os.getcwd()

# ---------- Basic Params ----------
data_filename = 'VOO_2020-10-15_2023-12-29.csv'
model_filename = 'VOO_2020-10-15_2023-12-29.pkl'
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
    pickle.dump(knn, file)
print(f"Model saved to {model_filename}")