import streamlit as st
import pandas as pd
from datetime import timedelta

# Sample task data (this can be loaded from a file instead)
data = {
    'Task': ['Task 1', 'Task 2', 'Task 3', 'Task 4'],
    'Date': [pd.Timestamp('2024-09-28'), pd.Timestamp('2024-10-01'), pd.Timestamp('2024-10-03'), pd.Timestamp('2024-10-05')],
    'Status': ['Pending', 'Pending', 'Pending', 'Pending']
}

# Load the data into a Pandas DataFrame
df = pd.DataFrame(data)

# Store updated task statuses in session state to keep track of changes
if 'statuses' not in st.session_state:
    st.session_state['statuses'] = df['Status'].tolist()

# Title
st.title("Task Management")

# Display the task management table with dropdowns in each row
st.write("### Task List")

# Initialize a container for the task table
with st.form(key='task_form'):
    updated_statuses = []
    
    # Create table headers
    st.write(f"{'Task':<20}{'Due Date':<20}{'Current Status':<20}")
    
    # Loop through tasks and create a row for each
    for i, row in df.iterrows():
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.write(f"{row['Task']}")

        with col2:
            st.write(f"{row['Date'].strftime('%Y-%m-%d')}")

        with col3:
            updated_statuses.append(
                st.selectbox(
                    f"Update status for {row['Task']}", 
                    ['Pending', 'Completed', 'Skipped', 'Next Week'], 
                    key=f"status_{i}", 
                    index=['Pending', 'Completed', 'Skipped', 'Next Week'].index(st.session_state['statuses'][i])
                )
            )

    # Button to submit changes
    submit_button = st.form_submit_button(label='Update Tasks')

# Function to move a task to next week
def move_task_to_next_week(task_index):
    df.at[task_index, 'Date'] += timedelta(weeks=1)

# When the "Update Tasks" button is clicked
if submit_button:
    for i in range(len(df)):
        selected_status = updated_statuses[i]
        df.at[i, 'Status'] = selected_status

        # If the task is moved to next week, update the due date
        if selected_status == 'Next Week':
            move_task_to_next_week(i)

    # Save the updated DataFrame to a CSV file
    df.to_csv('updated_tasks.csv', index=False)
    
    # Update the session state to reflect the new statuses
    st.session_state['statuses'] = updated_statuses

    # Success message
    st.success("Tasks updated successfully!")

# Display the updated table
st.write("### Updated Task List")
st.dataframe(df)

