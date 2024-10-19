import streamlit as st
from helpers import load_gsheet_data
def overview(sheet_url, sheet_name):
    current, worksheet = load_gsheet_data(sheet_url, sheet_name)
    st.write("### Debug: Current state of the CSV")
    st.dataframe(current, hide_index=True, height=1600, use_container_width=True)