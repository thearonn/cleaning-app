import streamlit as st
import pandas as pd
import math
from pathlib import Path
from data import closest_saturday
from datetime import datetime, timedelta
import csv
import copy

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    layout="centered",
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

# Add some styling for mobile responsiveness
st.markdown(
    """
    <style>
        /* Increase padding to avoid cutting off the title */
        .main .block-container {
            padding-top: 4rem;  /* Adjust top padding to avoid clipping */
            padding-left: 1rem;
            padding-right: 1rem;
        }

        /* Adjust text size for mobile */
        @media (max-width: 1000px) {
            h1, h2, h3, h4, h5, h6 {
                font-size: 50%;
            }
            .stButton button {
                width: 100%; /* Make buttons full-width on mobile */
            }

            /* Dataframe customization */
            .stDataFrame {
                font-size: 6px; /* Smaller font size for dataframe */
                width: 100% !important; /* Ensure the dataframe uses full width */
            }
            table {
                width: 100%;
            }
            th, td {
                padding: 4px; /* Reduce padding for better spacing */
                font-size: 12px; /* Adjust table font size */
            }
        }
    </style>
    """,
    unsafe_allow_html=True
)


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

this_week3 = pd.DataFrame(this_week["Task"])
# Initialize a container for the task table
with st.form(key='task_form'):
    updated_statuses = []
    
    # Create table headers
    st.write(f"{'Task':<20}{'Completed':<20}{'Skip':<20}{'Move':<20}")
    
    checkbox_completed = []
    checkbox_skipped = []
    checkbox_moved = []
    # Loop through tasks and create a row for each
    col1, col2, col3 , col4= st.columns([3, 1, 1,1])
    with col1:
        st.write("Task")
    with col2:
        st.write("Completed?")
    with col3:
        st.write("Skip")
    with col4:
        st.write("Move to next week")
    
    for i, row in this_week3.iterrows():
        

        with col1:
            st.write(f"{row['Task']}")

        with col2:
            checkbox_completed.append(st.checkbox("completed",key=f"checkbox_complete{i}", label_visibility="hidden"))
        
        with col3:
            checkbox_skipped.append(st.checkbox("skipped",key=f"checkbox_skip{i}", label_visibility="hidden"))
        
        with col4:
            checkbox_moved.append(st.checkbox("moved",key=f"checkbox_moved{i}", label_visibility="hidden"))
    submit_button = st.form_submit_button(label='Submit')


this_week3["Status"] = "Pending"
# Add custom radio buttons for task status
status_options = ['Pending', 'Completed', 'Skipped', 'Moved']

# Create a grid builder
gb = GridOptionsBuilder.from_dataframe(this_week3)

# Configure column "Status" to use radio buttons for user input
gb.configure_column("Status", editable=True, cellEditor='agSelectCellEditor', 
                    cellEditorParams={'values': status_options})

# Allow multiline wrapping for the 'Task' column
gb.configure_column("Task", wrapText=True, autoHeight=True)

# Create the grid options
grid_options = gb.build()

# Display the grid with the radio button column for status
grid_response = AgGrid(
    this_week3,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    allow_unsafe_jscode=True,
    height=300
)

# Access the updated DataFrame from the grid
updated_df = grid_response['data']

# Display the updated DataFrame when submitted
if st.button('Submit'):
    st.write("### Updated Task List")
    st.dataframe(updated_df)
