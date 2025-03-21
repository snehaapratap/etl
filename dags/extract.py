import pandas as pd

def extract_data():
    csv_data = pd.read_csv("data/train_schedule.csv")
    excel_data = pd.read_excel("data/train_schedule.xlsx")
    json_data = pd.read_json("data/train_schedule.json")

    return pd.concat([csv_data, excel_data], ignore_index=True)
