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
    
    return df

if __name__ == "__main__":
    print("Fetching train schedule data from PostgreSQL...")
    df = view_train_schedule() 