
import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px

# Adds the parent directory to the system path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from data_fetcher_streamlit_ import get_from_table_
import db_utils_.insert_data_to_clickhouse_table_ as insert_clickhouse_
import db_utils_.establish_connection_clickhouse_ as get_conn_
import db_utils_.db_commands_ as commands_
import db_utils_.establish_connection_clickhouse_ as clickhouse_connect
st.set_page_config(page_title="Inventory Explorer", page_icon="📦")
from pathlib import Path

import tomllib
parent_dir = Path(__file__).resolve().parent.parent
config_path = str(parent_dir / "pyproject.toml")
config_path = config_path.replace("\\", "/")
with open(config_path, "rb") as f:
    data = tomllib.load(f)
table_name_ = data["clickhouse-db"]["table_name_"]   # Nested entries (tables)
#--------------------------------------------------
# Involking data_fetcher_streamlit
df = get_from_table_()
df['Select'] = False
db_client_ = clickhouse_connect.get_clickhouse_client_()

#--------------------------------------------------
st.header('Application')
# Sidebar navigation
st.sidebar.page_link('py_login_page_streamlit_.py', label='Login')
st.sidebar.page_link('pages/app.py', label='Application')


#--------------------------------------------------
# Setting up the UI .. 
st.set_page_config(page_title="Incubyte Employee Directory Assignment", page_icon="⛄", layout="wide")
st.image("imgs_/ancestors.png", width=100)
st.title(" Employee Data Management")
st.write(
    "Modify, add, or delete employee data directly inside the table. Use the checkboxes to select specific rows."
)

if "show_add_form" not in st.session_state:
    st.session_state["show_add_form"] = False    

if "table_update" not in st.session_state:
    st.session_state["table_update"] = False    
    st.session_state["employee_df"] = df

if "reload_insights" not in st.session_state:
    st.session_state["reload_insights"] = False    
    
    
#--------------------------------------------------



#--------------------------------------------------
# Setting up the UI , Adding new row.. 
col1, col2, _ = st.columns([1, 1, 4])
with col1:
    if st.button("➕ Add New Row", width='stretch'):
        st.session_state["show_add_form"] = True
        st.rerun()


with col2:
    if st.button("🗑️ Delete Selected", width='stretch'):
        df = st.session_state["employee_df"]
        # Keep only the rows where the "Select" column checkbox is False
        if df["Select"].any():
            st.session_state["employee_df"] = df[~df["Select"]].reset_index(
                drop=True
            )
            st.success("Selected rows deleted successfully!")
            df_modified_ = st.session_state["employee_df"]
            df_modified_ = df_modified_.drop(columns='Select')

            insert_clickhouse_.refresh_dataframe_changes_in_frontend_\
                (the_client_=db_client_, this_table_ = table_name_, \
                the_modified_df_ = df_modified_)
            st.rerun()

        else:
            st.warning("Please check at least one row's box to delete.")

st.write("")  # Visual spacer

if st.session_state["show_add_form"]:
    st.write("")

    with st.container(border=True):
        st.subheader("📝 New Employee Details")
        st.info("All fields must be filled out before submitting.")

        f_col1, f_col2, f_col3, f_col4, f_col5  = st.columns(5)

        with f_col1:
            new_first = st.text_input("First Name", value="", placeholder="e.g. Bob").strip()
        with f_col2:
            new_last = st.text_input("Last Name", value="", placeholder="e.g. Brown").strip()
        with f_col3:
            # Using value=None ensures the input field starts completely blank
            new_salary = st.number_input("Salary", min_value=0, value=None, placeholder="e.g. 60000")
        with f_col4:
            new_loc = st.text_input("Location", value="", placeholder="e.g. Austin").strip()
        with f_col5:
            new_tz = st.text_input("TimeZone", value="", placeholder="e.g. GMT/BST (UTC+0 / UTC+1)").strip()

        # Submit & Cancel Button Row inside the container
        btn_col1, btn_col2, _ = st.columns([1, 1, 2])
        
        with btn_col1:
            if st.button("Submit Row", type="primary", use_container_width=True):
                # Validation check: Ensure absolutely nothing is left blank
                if not new_first or not new_last or new_salary is None or not new_loc:
                    st.error("⚠️ All columns are required! Please fill out every field.")
                else:
                    # Construct the new entry
                    new_row_df = pd.DataFrame([{
                        "First_Name": new_first,
                        "Last_Name": new_last,
                        "Gross_Salary": int(new_salary),
                        "Employee_Location": new_loc,
                        "Time_Zone": new_tz,
                        "Select": False
                    }])
                    
                    # Core Requirement: Concatenate with new row on TOP (index position 0)
                    
                    df = pd.concat([new_row_df, df], join='inner', ignore_index=True)
                    st.session_state["employee_df"] = df
                    st.session_state["table_update"] = True    
                    df_modified_ = st.session_state["employee_df"]
                    df_modified_ = df_modified_.drop(columns='Select')

                    insert_clickhouse_.refresh_dataframe_changes_in_frontend_\
                        (the_client_=db_client_, this_table_ = table_name_, \
                        the_modified_df_ = df_modified_)
                    st.rerun()
                    
                    # Close form and refresh layout
                    st.session_state["show_add_form"] = False
                    st.toast("🚀 New employee successfully injected at the top!", icon="✅")
                    st.rerun()

        with btn_col2:
            if st.button("Cancel", width='stretch'):
                st.session_state["show_add_form"] = False
                st.rerun()

st.write("---")

### Render the Scrollable Interactive Data Editor
### Assign a key so Streamlit captures updates automatically

edited_df = st.data_editor(
    st.session_state["employee_df"],
    width='stretch',
    num_rows="dynamic",  # Allows users to also use Streamlit's built-in bottom row addition feature
    hide_index=True,  # Hides pandas index integers for a cleaner UI
    column_config={
        "Select": st.column_config.CheckboxColumn(
            "Select",
            help="Check to select this employee row for bulk deletion",
            default=False,
        ),
        "Salary": st.column_config.NumberColumn(
            "Salary",
            format="%,d",  # Formats numbers nicely with commas and dollar signs
            min_value=0,
        ),
    },
)

#### Critical Step: Save any live on-screen cell edits back to Session State
st.session_state["employee_df"] = edited_df

#### Optional Metric Dashboard to show live data synchronization
st.write("---")
st.subheader("📊 Live Insights")
m_col1, m_col2, m_col3 = st.columns(3)

if not edited_df.empty:
    m_col1.metric("Total Employees", len(edited_df))
    m_col2.metric("Average Salary", f"${int(edited_df['Gross_Salary'].mean()):,}")
    m_col3.metric("Locations Active", edited_df["Employee_Location"].nunique())
else:
    st.info("The directory is currently empty.")

fig = px.pie(edited_df, values='Gross_Salary', names='Employee_Location', title='Salary Distribution : Location')
st.plotly_chart(fig)

location_arr_ = edited_df['Employee_Location'].unique()
salary_avg_val_ = edited_df.groupby('Employee_Location')['Gross_Salary'].mean()

fig = px.bar(x = location_arr_, y=salary_avg_val_, title="Average Salaries across locations", color=salary_avg_val_)
st.plotly_chart(fig)



fig = px.violin(
    edited_df, 
    x='Employee_Location',       # Unique locations on the x-axis
    y='Gross_Salary',         # Salary values on the y-axis
    color='Employee_Location',   # Distinct color for each location
    box=True,           # Displays a box plot inside to show median, quartiles, and range
    # points='all',       # Optional: shows all individual data points next to the violin
    title='Salary Distribution, Mean, and Variance by Location',
    labels={'location': 'Location', 'salary': 'Salary ($)'}
)

fig.update_traces(
    meanline_visible=True,  # Adds a dashed line indicating the mean salary
    box_visible=True        # Ensures the internal box plot is visible for range details
)

fig.update_layout(
    xaxis_title="Locations",
    yaxis_title="Salary Range ($)",
    showlegend=False,
    template="plotly_white"
)
st.plotly_chart(fig)

st.write("---")

