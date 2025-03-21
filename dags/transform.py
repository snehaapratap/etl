import pandas as pd
from extract import extract_data

def transform_data():
    df = extract_data()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    
    # Specify the time format explicitly
    time_format = "%H:%M:%S"
    df["departure_time"] = pd.to_datetime(df["departure_time"], format=time_format, errors="coerce")
    df["arrival_time"] = pd.to_datetime(df["arrival_time"], format=time_format, errors="coerce")
    
    df.drop_duplicates(inplace=True)
    # Use ffill() instead of fillna(method="ffill")
    df = df.ffill()
    
    return df
