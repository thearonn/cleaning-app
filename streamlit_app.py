import streamlit as st
import pandas as pd
import math
from pathlib import Path
from data import closest_saturday
from datetime import datetime, timedelta
import csv
import copy
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='Rengøring',
    page_icon=':broom:', # This is an emoji shortcode. Could be a URL too.
)


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# :broom: Nu skal vi gøre rent

'''

# Add some spacing
''
''
closest_sat = closest_saturday(datetime.today()).strftime("%d/%m")
st.header(f"Nærmeste lørdag er {closest_sat}")

current = pd.read_csv("current_state.csv")

this_week = current[current["Next due date"] == "2024-09-28"]

this_week = pd.DataFrame(this_week["Task"])
this_week["Status"] = "Pending"

st.dataframe(this_week)


st.data_editor(
    this_week,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            width="medium",
            options=[
                "Pending",
                "Completed",
                "Moved to next week",
            ],
            required=True,
        )
    },
    hide_index=True,
)

this_week2 = pd.DataFrame(this_week["Task"])
this_week2["Completed?"] = False
this_week2["Move to next week"] = False
this_week2["Skip"] = False
st.data_editor(
    this_week2,
    column_config={
        "Completed?": st.column_config.CheckboxColumn(
            "Completed?",
            default=False,
        )
    },
    disabled=["widgets"],
    hide_index=True,
)

st.dataframe(this_week2)
#st.data_editor(
#    this_week2,
#    column_config={
#        "Skip?": st.column_config.CheckboxColumn(
#            "Your favorite?",
#            help="Select your **favorite** widgets",
#            default=False,
#        )
#    },
#    disabled=["widgets"],
#    hide_index=True,
#)
#st.data_editor(
#    this_week2,
#    column_config={
#        "Move to next week": st.column_config.CheckboxColumn(
#            "Your favorite?",
#            help="Select your **favorite** widgets",
#            default=False,
#        )
#    },
#    disabled=["widgets"],
#    hide_index=True,
#)