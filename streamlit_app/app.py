import streamlit as st
import pandas as pd
import os
from sqlalchemy import create_engine

# PostgreSQL connection details
DB_URI = "postgresql://postgres:postgres@localhost:5432/postgres"

# Set page config
st.set_page_config(
    page_title="Indian Railways Train Schedule",
    page_icon="🚂",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 0rem 0rem;
    }
    .st-emotion-cache-18ni7ap {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True)

def get_train_data():
    try:
        engine = create_engine(DB_URI)
        return pd.read_sql("SELECT * FROM standardized_train_schedule", engine)
    except Exception as e:
        st.error(f"Error connecting to database: {str(e)}")
        return None

def main():
    # Header
    st.title("🚂 Indian Railways Train Schedule Dashboard")
    st.markdown("---")

    # File Upload Section
    st.sidebar.header("Upload New Data")
    uploaded_file = st.sidebar.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
    if uploaded_file:
        file_path = os.path.join("/Users/snehapratap/desktop/etl/data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.sidebar.success(f"File uploaded: {uploaded_file.name}")
        
        if st.sidebar.button("Trigger ETL Pipeline"):
            os.system("airflow dags trigger train_schedule_etl")
            st.sidebar.success("ETL pipeline triggered!")

    # Data Display Section
    df = get_train_data()
    if df is not None:
        # Overview Metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Trains", len(df))
        with col2:
            st.metric("Express Trains", len(df[df['train_type'] == 'Express']))
        with col3:
            st.metric("Daily Trains", len(df[df['days_of_operation'] == 'Daily']))
        with col4:
            st.metric("Total Routes", len(df[['source', 'destination']].drop_duplicates()))

        # Train Search Section
        st.subheader("🔍 Search Trains")
        col1, col2 = st.columns(2)
        with col1:
            source = st.selectbox("Select Source", sorted(df['source'].unique()))
        with col2:
            destination = st.selectbox("Select Destination", sorted(df['destination'].unique()))
        
        filtered_df = df[
            (df['source'] == source) & 
            (df['destination'] == destination)
        ]
        
        if not filtered_df.empty:
            st.dataframe(
                filtered_df[[
                    'train_number', 'train_name', 'arrival_time', 
                    'departure_time', 'travel_duration', 'days_of_operation', 
                    'train_type'
                ]],
                hide_index=True
            )
        else:
            st.info("No direct trains found for this route.")

        # Train Types Analysis
        st.subheader("📊 Train Types Distribution")
        col1, col2 = st.columns(2)
        with col1:
            train_types = df['train_type'].value_counts()
            st.bar_chart(train_types)
        
        with col2:
            operation_days = df['days_of_operation'].value_counts()
            st.bar_chart(operation_days)

        # Popular Routes
        st.subheader("🗺️ Popular Routes")
        popular_routes = df.groupby(['source', 'destination']).size().reset_index(name='count')
        popular_routes = popular_routes.sort_values('count', ascending=False).head(10)
        st.dataframe(popular_routes, hide_index=True)

        # Train Schedule Explorer
        st.subheader("🕒 Train Schedule Explorer")
        train_type_filter = st.multiselect(
            "Filter by Train Type",
            options=sorted(df['train_type'].unique()),
            default=sorted(df['train_type'].unique())
        )
        
        days_filter = st.multiselect(
            "Filter by Days of Operation",
            options=sorted(df['days_of_operation'].unique()),
            default=sorted(df['days_of_operation'].unique())
        )
        
        filtered_schedule = df[
            (df['train_type'].isin(train_type_filter)) &
            (df['days_of_operation'].isin(days_filter))
        ]
        
        st.dataframe(
            filtered_schedule[[
                'train_number', 'train_name', 'source', 'destination',
                'arrival_time', 'departure_time', 'travel_duration',
                'days_of_operation', 'train_type'
            ]],
            hide_index=True
        )

if __name__ == "__main__":
    main()

