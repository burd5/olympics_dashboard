import streamlit as st
import pandas as pd
from pandas import DataFrame
import plotly.express as px

@st.cache_data
def load_data(filepath: str)-> DataFrame:
    try:
        data = pd.read_csv(filepath)
        if data.empty:
            st.error("No data found in the CSV file.", icon="🚨")
        return data
    except FileNotFoundError:
        st.error(
            f"File not found: {filepath}. Please check the file path.",
            icon="🚨",
        )
    except pd.errors.EmptyDataError:
        st.error("No data found in the CSV file.", icon="🚨")
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}", icon="🚨")
    return pd.DataFrame()  # Return an empty DataFrame if any error occurs

def filter_data(df, selected_year, selected_season, selected_medal):
    filtered_df = df.copy()
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_season:
        filtered_df = filtered_df[filtered_df['Season'] == selected_season]
    if selected_medal:
        filtered_df = filtered_df[filtered_df['Medal'] == selected_medal]
    return filtered_df