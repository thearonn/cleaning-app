import streamlit as st
import pandas as pd
import math
from pathlib import Path
import pickle
import csv
from datetime import datetime, timedelta
def load_tasks(file):
    df = pd.read_excel(file, engine='openpyxl')
    return df

def closest_saturday(date):
    # Get the current weekday (Monday=0, Sunday=6)
    current_weekday = date.weekday()
    
    # Saturday is the 5th day of the week (Monday=0, Saturday=5)
    saturday_weekday = 5
    
    # Calculate the difference to the closest Saturday
    days_until_saturday = (saturday_weekday - current_weekday) % 7
    
    # If today is after Saturday (like on Sunday), move to next Saturday
    if days_until_saturday == 0:
        return date
    else:
        return date + timedelta(days=days_until_saturday)
