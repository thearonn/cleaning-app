import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from helpers import load_gsheet_data, save_to_gsheet


def next_week(closest_sat, current, worksheet):
    next_saturday = closest_sat + timedelta(days=7)
    next_saturday = next_saturday.strftime('%Y-%m-%d')
    next_week_df = current[current["Next due date"] == next_saturday]

    if (next_week_df["Dominant"] == "dominant").any() & (next_week_df["Dominant"] == "").any():
        current.loc[next_week["Dominant"] == "", "Next due date"] += timedelta(days=7)
        save_to_gsheet(worksheet, current)
        next_week_df = current[current["Next due date"] == next_saturday]

    st.dataframe(next_week_df[["Task", "Last done"]], hide_index=True)
    return current