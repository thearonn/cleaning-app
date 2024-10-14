import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from data import closest_saturday

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
tab1, tab2= st.tabs(["Denne uge", "Overview"])
# Get the closest Saturday
with tab1:
    closest_sat = closest_saturday(datetime.today())
    st.header(f'Nærmeste lørdag er {closest_sat.strftime("%d/%m")}')

    today = closest_sat.strftime('%Y-%m-%d')
    # Placeholder to display the task table
    table_placeholder = st.empty()  # This creates an empty container to hold the table later

    # Load the current state from CSV
    current = pd.read_csv("current_state.csv")

    # Ensure that "Next due date" is a datetime object
    current["Next due date"] = pd.to_datetime(current["Next due date"], format='%Y-%m-%d')

    if (current["Dominant"] == "dominant").any():
        current.loc[pd.isna(current["Dominant"]), "Next due date"] += timedelta(days=7)
        current.to_csv("current_state.csv", index=False)

    # Define a function to filter and display tasks for this week
    def display_table():
        this_week = current[current["Next due date"] == today]

        this_week = pd.DataFrame(this_week["Task"])
        this_week["Fixed"] = False
        this_week["Move"] = False

        if this_week.empty:
            table_placeholder.write("Du kan holde fri og drikke en kop kaffe")
            return
        else:
            # Return the table and the edited dataframe from data editor
            edited_df = table_placeholder.data_editor(
                this_week,
                column_config={
                    "Fixed": st.column_config.CheckboxColumn("Fixed", default=False),
                    "Move": st.column_config.CheckboxColumn("Move", default=False),
                },
                hide_index=True,
                use_container_width=True
            )
            return edited_df

    # Initial display of the table
    edited_df = display_table()

    try:
    # Update button
        if st.button("Update", type="primary"):
                # Backup the current CSV
            current.to_csv("copy_of_current.csv", index=False)

            # Iterate through the rows in the data editor
            for index, row in edited_df.iterrows():
                if row["Fixed"]:
                    st.write(f'Task "{row["Task"]}" is marked as fixed.')
                    # Find the task in the original dataframe
                    task_index = current[current["Task"] == row["Task"]].index[0]

                    # Get the next due date and frequency (weeks) for this task
                    next_due_date = pd.to_datetime(current.loc[task_index, "Next due date"], format='%Y-%m-%d')
                    frequency_in_weeks = int(current.loc[task_index, "Frequency"])

                    # Update the "Last done" date to the current "Next due date"
                    current.loc[task_index, "Last done"] = next_due_date.strftime('%Y-%m-%d')

                    # If the task has been moved
                    if not pd.isna(current.loc[task_index, "Moved from"]):
                        new_next_due_date = pd.to_datetime(current.loc[task_index, "Moved from"], format='%Y-%m-%d') + timedelta(weeks=frequency_in_weeks)
                        # If the task occur every week OR have been moved multiple times.
                        if new_next_due_date <= next_due_date:
                            new_next_due_date = pd.to_datetime(current.loc[task_index, "Moved from"], format='%Y-%m-%d') + timedelta(weeks=frequency_in_weeks)
                        current.loc[task_index, "Moved from"] = ""
                    else:
                        new_next_due_date = next_due_date + timedelta(weeks=frequency_in_weeks)
                    current.loc[task_index, "Next due date"] = new_next_due_date.strftime('%Y-%m-%d')

                elif row["Move"]:
                    st.write(f'Task "{row["Task"]}" is marked to move to another day.')
                    task_index = current[current["Task"] == row["Task"]].index[0]

                    next_due_date = pd.to_datetime(current.loc[task_index, "Next due date"], format='%Y-%m-%d')
                    if pd.isna(current.loc[task_index, "Moved from"]):
                        current.loc[task_index, "Moved from"] = next_due_date

                    # Calculate and update the new "Next due date"
                    new_next_due_date = next_due_date + timedelta(weeks=1)
                    current.loc[task_index, "Next due date"] = new_next_due_date.strftime('%Y-%m-%d')


            # Save the updated DataFrame to the CSV
            current.to_csv("current_state.csv", index=False)

            # Filter and display the updated table
            edited_df = display_table()  # This will re-render the table with updated tasks
    except:
        st.write("Ups, du glemte at klikke noget af :clown_face:")

    if st.button("Skip uge :pig:"):
        st.write("Dovne svin")
         # Add 7 days to all "Next due date" values
        current["Next due date"] = pd.to_datetime(current["Next due date"], format='%Y-%m-%d') + timedelta(days=7)

        # Save the updated DataFrame to the CSV
        current.to_csv("current_state.csv", index=False)
        table_placeholder.write("Du kan holde fri og drikke en kop kaffe")

with tab2:
    st.write("### Debug: Current state of the CSV")
    st.dataframe(current)

