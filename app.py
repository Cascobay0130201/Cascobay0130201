
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(page_title="Casco Bay PV Tracker", layout="wide")

st.title("🚢 USCG Aux Casco Bay Flotilla 013-02-01")
st.subheader("Program Visitation Management System")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv('Program_Partner_Database.csv')

def save_data(df):
    df.to_csv('Program_Partner_Database.csv', index=False)

df = load_data()

# Sidebar - Filter/Search
st.sidebar.header("Search & Filter")
search_query = st.sidebar.text_input("Search Partner Name")
pv_filter = st.sidebar.selectbox("Filter by Assigned PV", ["All"] + sorted(df['Assigned_PV'].unique().tolist()))

# Apply filters
filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df['Partner_Name'].str.contains(search_query, case=False, na=False)]
if pv_filter != "All":
    filtered_df = filtered_df[filtered_df['Assigned_PV'] == pv_filter]

# Main UI
tab1, tab2 = st.tabs(["Partner List", "Update Visit"])

with tab1:
    st.dataframe(filtered_df, use_container_width=True)

with tab2:
    st.write("### Record a New Visit or Update Info")
    partner_to_update = st.selectbox("Select Partner", df['Partner_Name'].tolist())
    
    if partner_to_update:
        # Get current row
        row_idx = df.index[df['Partner_Name'] == partner_to_update].tolist()[0]
        current_data = df.iloc[row_idx]
        
        col1, col2 = st.columns(2)
        
        with col1:
            new_pv = st.text_input("Assigned PV", value=str(current_data['Assigned_PV']) if pd.notnull(current_data['Assigned_PV']) else "")
            new_date = st.date_input("Visit Date", value=date.today())
            new_next_visit = st.date_input("Next Scheduled Visit", value=date.today())
            
        with col2:
            new_status = st.selectbox("Status", ["Active", "Inactive", "Suspended"], index=0)
            new_notes = st.text_area("Visit Notes", value="")
            
        if st.button("Save Updates"):
            df.at[row_idx, 'Assigned_PV'] = new_pv
            df.at[row_idx, 'Last_Visit_Date'] = str(new_date)
            df.at[row_idx, 'Last_Visit_Notes'] = new_notes
            df.at[row_idx, 'Next_Scheduled_Visit'] = str(new_next_visit)
            df.at[row_idx, 'Partner_Status'] = new_status
            
            save_data(df)
            st.success(f"Updated {partner_to_update} successfully!")
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.info("This system allows PVs to coordinate visits and share information in real-time.")
