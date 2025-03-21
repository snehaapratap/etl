import pandas as pd

def extract_data():
    csv_data = pd.read_csv("/opt/airflow/dags/data/train_schedule.csv")
    excel_data = pd.read_excel("/opt/airflow/dags/data/train_schedule.xlsx")
    return pd.concat([csv_data, excel_data], ignore_index=True)
