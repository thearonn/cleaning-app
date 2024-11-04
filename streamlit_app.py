import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from helpers import closest_saturday
from tabs.this_week import this_week
from tabs.new_tasks import add_new_tasks
from tabs.next_week import next_week
from tabs.task_overview import overview
from helpers import load_gsheet_data, save_to_gsheet

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    layout="centered",
    page_title='Rengøring',
    page_icon=':broom:',  # This is an emoji shortcode.
)

# Set the title that appears at the top of the page.
'''
# :broom: Nu skal vi gøre rent
'''

# Add some spacing
''
''

tab1, tab2, tab3, tab_overview= st.tabs(["Denne uge", "Hvad skal vi næste uge", "Tilføj nye opgaver","Overview"])
# Get the closest Saturday
closest_sat = closest_saturday(datetime.today())
sheet_url = "https://docs.google.com/spreadsheets/d/1TsUeKjOKdTfHLi4jaczyzPsscrDBj_Yue-kRlQzpbEU/edit?gid=235400169#gid=235400169"
sheet_name = "current_state"  

current, worksheet = load_gsheet_data(sheet_url=sheet_url, sheet_name=sheet_name)
print("Loader igen")
        
with tab1:
    print("running tab 1")
    print(current)

    current = this_week(closest_sat, current, worksheet)

with tab2:
    print("running tab2")
    current = next_week(closest_sat, current, worksheet)

with tab3:
   add_new_tasks(sheet_url, sheet_name)

with tab_overview:
   overview(sheet_url, sheet_name)
