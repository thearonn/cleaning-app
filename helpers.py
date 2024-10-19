import streamlit as st
import pandas as pd
import math
from pathlib import Path
import pickle
import csv

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime, timedelta
def load_tasks(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

@st.cache_resource
def authenticate_gsheets():
    # Define the scope for Google Sheets and Google Drive access
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    # Load service account credentials from JSON file
    creds = ServiceAccountCredentials.from_json_keyfile_name('service_account_credentials.json', scope)
    
    # Authorize the gspread client with the credentials
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