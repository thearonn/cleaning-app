import streamlit as st
import pandas as pd

# Sample task data
data = {
    'Task': [
        'Task 1: A long description of task 1 that might wrap onto multiple lines.',
        'Task 2: A simple task',
        'Task 3: This is task 3 with some longer description.',
        'Task 4: Task 4 description might be long as well.'
    ],
    'Status': ['Pending', 'Pending', 'Pending', 'Pending']  # Default status for each task
}

# Load the data into a Pandas DataFrame
df = pd.DataFrame(data)

# Title
st.title("Task Management (Completed, Skipped, Moved)")

# Initialize status list to store radio button choices
status_choices = []

# Create form to display tasks and status options
with st.form(key='task_form'):
    st.write("### Task List")

    # Loop through each task and create radio buttons for "Completed", "Skipped", "Moved"
    for i, row in df.iterrows():
        task_description = row['Task']
        current_status = row['Status']  # Default status

        # Display the task description
        st.write(f"**{task_description}**")

        # Create radio buttons for each task to select "Completed", "Skipped", or "Moved"
        status = st.radio(
            label=f"Status for Task {i+1}",  # Unique label for each task's radio button group
            options=['Pending', 'Completed', 'Skipped', 'Moved'],  # Possible status options
            index=0 if current_status == 'Pending' else ['Pending', 'Completed', 'Skipped', 'Moved'].index(current_status),  # Preselect current status
            key=f"radio_{i}"  # Unique key for each task's radio button
        )
        status_choices.append(status)  # Store the status selected for each task

    # Submit button
    submit_button = st.form_submit_button(label="Update")

# If the form is submitted, update the DataFrame with the selected statuses
if submit_button:
    df['Status'] = status_choices
    st.write("### Updated Task List")
    st.dataframe(df)
