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
    current_weekday = date.weekday()
    time_delta = 5-current_weekday if 5-current_weekday < 4 else 5-current_weekday-7
    return date + (timedelta(time_delta))