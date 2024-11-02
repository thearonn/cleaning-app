import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from helpers import load_gsheet_data, save_to_gsheet

def this_week(closest_sat, sheet_url, sheet_name):
    st.header(f'Nærmeste lørdag er {closest_sat.strftime("%d/%m")}')

    today = closest_sat.strftime('%Y-%m-%d')
    # Placeholder to display the task table
    table_placeholder = st.empty()  # This creates an empty container to hold the table later

    current, worksheet = load_gsheet_data(sheet_url=sheet_url, sheet_name=sheet_name)

    # Ensure that "Next due date" is a datetime object
    current["Next due date"] = pd.to_datetime(current["Next due date"], format='%Y-%m-%d')

    this_week = current[current["Next due date"] == today]
    if (this_week["Dominant"] == "dominant").any() & (this_week["Dominant"] == "").any():
        current.loc[current["Dominant"] == "", "Next due date"] += timedelta(days=7)
        this_week = current[current["Next due date"] == today]

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
            unique_key = f"this_week_data_editor_{datetime.now().timestamp()}"
            edited_df = table_placeholder.data_editor(
                this_week,
                key = unique_key,
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
    a = 2
    if a == 2:
    #try:
    # Update button
        if st.button("Update", type="primary"):
                # Backup the current CSV
            save_to_gsheet(worksheet, current)

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
                    if not current.loc[task_index, "Moved from"] == "":
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
                    if current.loc[task_index, "Moved from"] == "":
                        current.loc[task_index, "Moved from"] = next_due_date

                    # Calculate and update the new "Next due date"
                    new_next_due_date = next_due_date + timedelta(weeks=1)
                    current.loc[task_index, "Next due date"] = new_next_due_date.strftime('%Y-%m-%d')


            # Save the updated DataFrame to the CSV
            date_columns = ["Next due date", "Last done", "Moved from"]
            for col in date_columns:
                if col in current.columns:
                    current[col] = current[col].astype(str)
            save_to_gsheet(worksheet, current)

            # Filter and display the updated table
            edited_df = display_table()  # This will re-render the table with updated tasks
    #except:
    #    st.write("Ups, du glemte at klikke noget af :clown_face:")

    if st.button("Skip uge :pig:"):
        st.write("Dovne svin")
         # Add 7 days to all "Next due date" values
        current["Next due date"] = pd.to_datetime(current["Next due date"], format='%Y-%m-%d') + timedelta(days=7)

        # Save the updated DataFrame to the CSV
        save_to_gsheet(worksheet, current)
        table_placeholder.write("Du kan holde fri og drikke en kop kaffe")