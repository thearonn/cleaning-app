import streamlit as st
import pandas as pd
import math
from pathlib import Path
import pickle
import csv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime, timedelta
def load_tasks(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df


import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json

# Step 1: Authenticate Google Sheets API based on environment
@st.cache_resource
def authenticate_gsheets():
    # Define the scope for Google Sheets and Google Drive access
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    try:
        service_account_info = {
            "type": "service_account",
            "project_id": st.secrets["project_id"],
            "private_key_id": st.secrets["private_key_id"],
            "private_key": st.secrets["private_key"].replace("\\n", "\n"),
            "client_email": st.secrets["client_email"],
            "client_id": st.secrets["client_id"],
            "auth_uri": st.secrets["auth_uri"],
            "token_uri": st.secrets["token_uri"],
            "auth_provider_x509_cert_url": st.secrets["auth_provider_x509_cert_url"],
            "client_x509_cert_url": st.secrets["client_x509_cert_url"]
        }
        creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    except FileNotFoundError:
        # Running locally - load credentials from the .json file
        creds = ServiceAccountCredentials.from_json_keyfile_name("service_account_credentials.json", scope)

    # Authorize with the gspread client
    client = gspread.authorize(creds)
    return client



def closest_saturday(date):
    current_weekday = date.weekday()
    time_delta = 5-current_weekday if 5-current_weekday < 4 else 5-current_weekday-7
    return date + (timedelta(time_delta))

def load_gsheet_data(sheet_url, sheet_name):
    client = authenticate_gsheets()
    
    # Open the Google Sheet by URL
    sheet = client.open_by_url(sheet_url)
    
    # Access the specific worksheet by name
    worksheet = sheet.worksheet(sheet_name)
    
    # Get all data from the sheet
    data = worksheet.get_all_values()
    
    # Convert data to pandas DataFrame (exclude header row if needed)
    df = pd.DataFrame(data[1:], columns=data[0])  # [1:] skips the header row
    return df, worksheet

# Step 3: Save a modified pandas DataFrame back to Google Sheets
def save_to_gsheet(worksheet, df):
    df = df.copy()  # Avoid modifying the original DataFrame
    for col in df.select_dtypes(include=['datetime64']):
        df[col] = df[col].dt.strftime('%Y-%m-%d')
    # Update the entire worksheet with the new DataFrame data
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())