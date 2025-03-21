import pandas as pd

def transform_data():
    df = extract_data()
    df.columns = df.columns.str.lower().str.replace(" ", "_")
    df["departure_time"] = pd.to_datetime(df["departure_time"], errors="coerce")
    df["arrival_time"] = pd.to_datetime(df["arrival_time"], errors="coerce")
    df.drop_duplicates(inplace=True)
    df.fillna(method="ffill", inplace=True)
    return df
