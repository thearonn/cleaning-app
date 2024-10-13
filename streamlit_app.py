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


closest_sat = closest_saturday(datetime.today()).strftime("%d/%m")
st.header(f"Nærmeste lørdag er {closest_sat}")

current = pd.read_csv("current_state.csv")

this_week = current[current["Next due date"] == "2024-09-28"]

this_week = pd.DataFrame(this_week["Task"])


this_week["Fixed"] = False
this_week["Move"] = False
this_week["Skip"] = False

# Display the data editor
edited_df = st.data_editor(
    this_week,
    column_config={
        "Fixed": st.column_config.CheckboxColumn("Fixed", default=False),
        "Move": st.column_config.CheckboxColumn("Move", default=False),
        "Skip": st.column_config.CheckboxColumn("Skip", default=False),
    },
    hide_index=True,
    use_container_width=True
)

# Update button
if st.button("Update"):
    # Iterate through the rows and process them based on the checkbox values
    for index, row in edited_df.iterrows():
        if row["Fixed"]:
            st.write(f'Task "{row["Task"]}" is marked as fixed.')
            # Process fixed task
        elif row["Move"]:
            st.write(f'Task "{row["Task"]}" is marked to move to another day.')
            # Process move task
        elif row["Skip"]:
            st.write(f'Task "{row["Task"]}" is marked to be skipped.')
            # Process skipped task