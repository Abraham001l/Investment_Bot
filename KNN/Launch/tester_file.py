from data_collection_module import update_dataset
# import os
# import pandas as pd

# cur_dir = os.getcwd()

# data_filename = 'VOO_all.csv'
# data_filename = os.path.join(cur_dir, 'KNN\\Development\\Datasets', data_filename)

update_dataset('VOO')
# data = pd.read_csv(data_filename)
# print(data.iloc[-1])