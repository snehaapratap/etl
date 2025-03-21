import pandas as pd
from sqlalchemy import create_engine

# PostgreSQL connection details
DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"

def view_train_schedule():
    # Create database connection
    engine = create_engine(DB_URI)
    
    # Query the data
    query = "SELECT * FROM standardized_train_schedule"
    df = pd.read_sql(query, engine)
    
    # Display basic information
    print("\nDataset Info:")
    print("-" * 50)
    print(f"Total Records: {len(df)}")
    print(f"Columns: {', '.join(df.columns)}")
    
    # Display first few records
    print("\nFirst 5 Records:")
    print("-" * 50)
    print(df.head())
    
    # Display summary statistics
    print("\nSummary Statistics:")
    print("-" * 50)
    print(df.describe())
    
    # Display Express Trains
    print("\nExpress Trains:")
    print("-" * 50)
    express_trains = pd.read_sql("SELECT * FROM standardized_train_schedule WHERE train_type = 'Express'", engine)
    print(f"Total Express Trains: {len(express_trains)}")
    print(express_trains[['train_number', 'train_name', 'source', 'destination', 'train_type']].head())
    
    # Display Trains between Mumbai Central and New Delhi
    print("\nTrains between Mumbai Central and New Delhi:")
    print("-" * 50)
    mumbai_delhi = pd.read_sql("SELECT * FROM standardized_train_schedule WHERE source = 'Mumbai Central' AND destination = 'New Delhi'", engine)
    print(f"Total Trains on this route: {len(mumbai_delhi)}")
    print(mumbai_delhi[['train_number', 'train_name', 'travel_duration', 'days_of_operation']].head())
    
    # Display Daily Trains
    print("\nDaily Operating Trains:")
    print("-" * 50)
    daily_trains = pd.read_sql("SELECT * FROM standardized_train_schedule WHERE days_of_operation = 'Daily'", engine)
    print(f"Total Daily Trains: {len(daily_trains)}")
    print(daily_trains[['train_number', 'train_name', 'source', 'destination']].head())
    
    return df

if __name__ == "__main__":
    print("Fetching train schedule data from PostgreSQL...")
    df = view_train_schedule() 