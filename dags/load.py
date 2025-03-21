from sqlalchemy import create_engine
import pandas as pd
from transform import transform_data

DB_URI = "mysql+pymysql://airflow:airflow@mysql/train_schedule"

def load_data():
    df = transform_data()
    engine = create_engine(DB_URI)
    df.to_sql("standardized_train_schedule", con=engine, if_exists="replace", index=False)
