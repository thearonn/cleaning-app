import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from helpers import load_gsheet_data, save_to_gsheet

def add_new_tasks(sheet_url, sheet_name):
    st.title('Tilføj en opgave')

    # Input fields
    task_name = st.text_input("Hvad er opgaven?")
    task_date = st.date_input("Hvornår skal det gøres næste gang? (skal være en lørdag)", value=datetime.today())
    task_frequency = st.text_input("Hvor ofte skal det gøres? Antal uger imellem.")
    task_type = st.selectbox("Er det en dominant opgave, gentagende opgave eller almindelig opgave?", ["normal","dominant", "gentagende"])
    
    if task_type == "normal":
        dominant = None
    elif task_type == "dominant":
        dominant = "dominant"
    elif task_type == "gentagende":
        dominant = "reccuring"
    # Submit button
    if st.button('Submit'):

        st.write("**Task Name**:", task_name)
        st.write("**Next Due Date**:", task_date)
        st.write("**Frequency**:", task_frequency)
        st.write("**Task Type**:", task_type)
        
        new_row = {
        "Task": task_name,
        "Next due date": task_date.strftime('%Y-%m-%d'),
        "Last done": None,
        "Frequency": task_frequency,
        "Dominant": dominant,
        "Moved from": None
        }

        # Load the existing CSV file
        df, worksheet = load_gsheet_data(sheet_url, sheet_name)
        # Append the new row
        df = df.append(new_row, ignore_index=True)
    
        save_to_gsheet(worksheet, df)
    
        st.write("Task added to CSV!")