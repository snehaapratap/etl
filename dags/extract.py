import os
import pandas as pd

# Use relative path from the DAG file location
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

def extract_data():
    csv_file = os.path.join(DATA_DIR, "train_schedule.csv")
    excel_file = os.path.join(DATA_DIR, "train_schedule.xlsx")
    json_file = os.path.join(DATA_DIR, "train_schedule.json")

    if not os.path.exists(csv_file) or not os.path.exists(excel_file) or not os.path.exists(json_file):
        raise FileNotFoundError(f"CSV or Excel file not found in the data folder! Looking in: {DATA_DIR}")

    csv_data = pd.read_csv(csv_file)
    excel_data = pd.read_excel(excel_file)
    json_data = pd.read_json(json_file)
    
    return pd.concat([csv_data, excel_data, json_data], ignore_index=True)
