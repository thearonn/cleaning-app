import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from helpers import load_gsheet_data, save_to_gsheet


def next_week(closest_sat, sheet_url, sheet_name):
    next_saturday = closest_sat + timedelta(days=7)
    st.header(f'Næste lørdag er {next_saturday.strftime("%d/%m")}')
    next_saturday = next_saturday.strftime('%Y-%m-%d')
    # Placeholder to display the task table
    table_placeholder = st.empty()  # This creates an empty container to hold the table later
    # Load the current state from CSV
    next_week, worksheet = load_gsheet_data(sheet_url, sheet_name)
    # Ensure that "Next due date" is a datetime object
    next_week["Next due date"] = pd.to_datetime(next_week["Next due date"], format='%Y-%m-%d')
    next_week_filtered = next_week[next_week["Next due date"] == next_saturday]
    if (next_week_filtered["Dominant"] == "dominant").any() & (next_week_filtered["Dominant"] == "").any():
        next_week.loc[next_week["Dominant"] == "", "Next due date"] += timedelta(days=7)
        save_to_gsheet(worksheet, next_week)
    next_week_filtered = next_week[next_week["Next due date"] == next_saturday]
    st.dataframe(next_week_filtered[["Task", "Last done"]], hide_index=True)