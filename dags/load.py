import os
from sqlalchemy import create_engine
import pandas as pd
from transform import transform_data

# PostgreSQL connection details (using Astro's Postgres container)
DB_URI = "postgresql://postgres:postgres@postgres:5432/postgres"

def load_data():
    df = transform_data()
    engine = create_engine(DB_URI)
    df.to_sql("standardized_train_schedule", con=engine, if_exists="replace", index=False)
    return "Data loaded successfully"

def query_express_trains():
    engine = create_engine(DB_URI)
    query = "SELECT * FROM standardized_train_schedule WHERE train_type = 'Express';"
    result = engine.execute(query)
    return result.fetchall()

def query_trains_between_cities():
    engine = create_engine(DB_URI)
    query = "SELECT * FROM standardized_train_schedule WHERE source = 'Mumbai Central' AND destination = 'New Delhi';"
    result = engine.execute(query)
    return result.fetchall()

def query_daily_trains():
    engine = create_engine(DB_URI)
    query = "SELECT * FROM standardized_train_schedule WHERE days_of_operation = 'Daily';"
    result = engine.execute(query)
    return result.fetchall()
