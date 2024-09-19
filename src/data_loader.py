# data_loader.py

import os
import pandas as pd
from datetime import datetime


def get_subdirectories(base_dir):
    return [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))]


def load_data(directory):
    csv_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == 'results.csv':
                csv_files.append(os.path.join(root, file))

    all_data = []
    for file in csv_files:
        df = pd.read_csv(file)
        # Extract timestamp from the file path
        timestamp = file.split(os.path.sep)[-2]
        df['file_timestamp'] = datetime.strptime(timestamp, "%Y-%m-%d-%H-%M-%S")
        all_data.append(df)

    return pd.concat(all_data, ignore_index=True) if all_data else pd.DataFrame()
