import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page config
st.set_page_config(page_title="Kenyan NSE Dashboard", layout="wide")

# Load data with caching
@st.cache_data
def load_data(file_path="Data.csv"):
    df = pd.read_csv(file_path, thousands=',', dtype={'Volume': str})
    # Clean Volume: remove commas and convert to numeric
    df['Volume'] = df['Volume'].str.replace(',', '').str.strip()
    df['Volume'] = pd.to_numeric(df['Volume'], errors='coerce').fillna(0).astype(int)
    # Clean Change% column: replace '-' with 0
    df['Change%'] = pd.to_numeric(df['Change%'], errors='coerce').fillna(0)
    # Convert Date to datetime
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y')
    # Filter out index rows (those with Code starting with '^') and keep only stock data
    df = df[~df['Code'].str.startswith('^')].copy()
    # Ensure numeric columns
    numeric_cols = ['12m Low', '12m High', 'Day Low', 'Day High', 'Day Price', 'Previous', 'Change']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")
# Date range
min_date = df['Date'].min()
max_date = df['Date'].max()
date_range = st.sidebar.date_input(
    "Date Range",
    value=[min_date, max_date],
    min_value=min_date,
    max_value=max_date
)
if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date, end_date = min_date, max_date
# Stock code multiselect
codes = st.sidebar.multiselect(
    "Select Stock Code(s)",
    options=df['Code'].unique(),
    default=df['Code'].unique()[:5]  # default to first 5 for performance
)
# Optional: filter by Name contains
name_filter = st.sidebar.text_input("Search by Name (contains)", "")

# Apply filters
filtered_df = df[(df['Date'] >= pd.to_datetime(start_date)) & (df['Date'] <= pd.to_datetime(end_date))]
if codes:
    filtered_df = filtered_df[filtered_df['Code'].isin(codes)]
if name_filter:
    filtered_df = filtered_df[filtered_df['Name'].str.contains(name_filter, case=False)]

# Check if data is empty after filters
if filtered_df.empty:
    st.warning("No data matches the selected filters. Please adjust filters.")
    st.stop()

# KPIs
st.header("Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
total_volume = filtered_df['Volume'].sum()
avg_day_price = filtered_df['Day Price'].mean()
max_day_high = filtered_df['Day High'].max()
num_stocks = filtered_df['Code'].nunique()
col1.metric("Total Volume (shares)", f"{total_volume:,.0f}")
col2.metric("Average Day Price", f"KES {avg_day_price:,.2f}")
col3.metric("Max Day High", f"KES {max_day_high:,.2f}")
col4.metric("Number of Stocks", num_stocks)

# Additional KPIs row
col5, col6, col7, col8 = st.columns(4)
total_turnover = (filtered_df['Day Price'] * filtered_df['Volume']).sum()
avg_change_pct = filtered_df['Change%'].mean()
col5.metric("Estimated Turnover", f"KES {total_turnover:,.0f}")
col6.metric("Avg Change %", f"{avg_change_pct:.2f}%")
# Convert dates to strings for metric display
col7.metric("Earliest Date", filtered_df['Date'].min().strftime("%Y-%m-%d"))
col8.metric("Latest Date", filtered_df['Date'].max().strftime("%Y-%m-%d"))

# Charts
st.subheader("Price Trends")
# Line chart: Day Price over time for selected codes
fig_line = px.line(filtered_df, x='Date', y='Day Price', color='Code',
                   title="Day Price Evolution",
                   labels={'Day Price': 'Price (KES)', 'Date': 'Date'})
st.plotly_chart(fig_line, use_container_width=True)

# Bar chart: Volume by stock
volume_by_code = filtered_df.groupby('Code')['Volume'].sum().reset_index()
fig_bar = px.bar(volume_by_code, x='Code', y='Volume', title="Total Volume per Stock",
                 labels={'Volume': 'Total Volume', 'Code': 'Stock Code'})
st.plotly_chart(fig_bar, use_container_width=True)

# Heatmap: average price by day of week and stock
st.subheader("Average Day Price by Weekday")
filtered_df['Weekday'] = filtered_df['Date'].dt.day_name()
pivot = filtered_df.pivot_table(index='Code', columns='Weekday', values='Day Price', aggfunc='mean')
fig_heat = px.imshow(pivot, text_auto=True, aspect="auto", color_continuous_scale='Viridis',
                     title="Average Day Price by Stock and Weekday")
st.plotly_chart(fig_heat, use_container_width=True)

# Top gainers/losers
st.subheader("Top Gainers & Losers (Latest Date)")
latest_date = filtered_df['Date'].max()
latest_data = filtered_df[filtered_df['Date'] == latest_date].copy()
if not latest_data.empty:
    latest_data = latest_data.sort_values('Change%', ascending=False)
    col_gain, col_loss = st.columns(2)
    with col_gain:
        st.write("**Top Gainers**")
        st.dataframe(latest_data[['Code', 'Name', 'Day Price', 'Change%']].head(5), use_container_width=True)
    with col_loss:
        st.write("**Top Losers**")
        st.dataframe(latest_data[['Code', 'Name', 'Day Price', 'Change%']].tail(5).sort_values('Change%'), use_container_width=True)
else:
    st.info("No data for the latest date in filtered results.")

# Data table
st.subheader("Filtered Data")
st.dataframe(filtered_df, use_container_width=True)

# Download button
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv(index=False).encode('utf-8')

csv = convert_df_to_csv(filtered_df)
st.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name='nse_filtered_data.csv',
    mime='text/csv',
)

st.sidebar.info("This dashboard uses data from the Kenyan NSE. Use filters to explore stock performance.")
