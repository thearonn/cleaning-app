import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from helpers import closest_saturday
from tabs.this_week import this_week
from tabs.new_tasks import add_new_tasks
from tabs.next_week import next_week
from tabs.task_overview import overview


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

with tab1:
    this_week(closest_sat, sheet_url, sheet_name)

with tab2:
    next_week(closest_sat, sheet_url, sheet_name)

with tab3:
   add_new_tasks(sheet_url, sheet_name)

with tab_overview:
   overview(sheet_url, sheet_name)
