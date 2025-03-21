import streamlit as st
import pandas as pd
import os

UPLOAD_DIR = "uploads/"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

st.title("Indian Railways Train Schedule ETL")

uploaded_file = st.file_uploader("Upload CSV or Excel file", type=["csv", "xlsx"])
if uploaded_file:
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"File uploaded: {file_path}")
    st.write("Triggering ETL pipeline...")
    
    os.system("airflow dags trigger train_schedule_etl")
    st.success("ETL pipeline triggered!")
