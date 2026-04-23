import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("Data.csv")

    # Clean data
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Volume'] = df['Volume'].str.replace(',', '').replace('-', '0').astype(float)
    df['Change%'] = df['Change%'].str.replace('%', '').replace('-', '0').astype(float)

    return df

df = load_data()

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.title("Filters")

# Date filter
date_range = st.sidebar.date_input(
    "Select Date Range",
    [df['Date'].min(), df['Date'].max()]
)

# Stock filter
stock_list = df['Code'].unique()
selected_stock = st.sidebar.multiselect("Select Stock Code", stock_list, default=stock_list)

# Apply filters
filtered_df = df[
    (df['Date'] >= pd.to_datetime(date_range[0])) &
    (df['Date'] <= pd.to_datetime(date_range[1])) &
    (df['Code'].isin(selected_stock))
]

# -----------------------------
# Dashboard Title
# -----------------------------
st.title("📈 Kenyan NSE Dashboard")

# -----------------------------
# KPIs
# -----------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

avg_price = filtered_df['Day Price'].mean()
total_volume = filtered_df['Volume'].sum()

top_gainer = filtered_df.loc[filtered_df['Change%'].idxmax()] if not filtered_df.empty else None
top_loser = filtered_df.loc[filtered_df['Change%'].idxmin()] if not filtered_df.empty else None

col1.metric("Avg Price", f"{avg_price:.2f}")
col2.metric("Total Volume", f"{total_volume:,.0f}")

if top_gainer is not None:
    col3.metric("Top Gainer", f"{top_gainer['Code']} ({top_gainer['Change%']}%)")

if top_loser is not None:
    col4.metric("Top Loser", f"{top_loser['Code']} ({top_loser['Change%']}%)")

# -----------------------------
# Price Trend
# -----------------------------
st.subheader("Price Trend")

fig_price = px.line(
    filtered_df,
    x='Date',
    y='Day Price',
    color='Code',
    title="Stock Price Over Time"
)

st.plotly_chart(fig_price, use_container_width=True)

# -----------------------------
# Volume Chart
# -----------------------------
st.subheader("Trading Volume")

fig_vol = px.bar(
    filtered_df,
    x='Code',
    y='Volume',
    color='Code',
    title="Volume by Stock"
)

st.plotly_chart(fig_vol, use_container_width=True)

# -----------------------------
# Gainers vs Losers
# -----------------------------
st.subheader("Market Movers")

fig_change = px.bar(
    filtered_df.sort_values('Change%', ascending=False),
    x='Code',
    y='Change%',
    color='Change%',
    title="Percentage Change"
)

st.plotly_chart(fig_change, use_container_width=True)

# -----------------------------
# Raw Data Table
# -----------------------------
st.subheader("Filtered Data")
st.dataframe(filtered_df)import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Setup Page Configuration
st.set_page_config(page_title="NSE Kenya Dashboard", layout="wide")

st.title("🇰🇪 Nairobi Securities Exchange (NSE) Analytics")
st.markdown("Monitor performance and trends of Kenyan stocks.")

# 2. Load Data (Replace with your actual NSE data source)
@st.cache_data
def load_data():
    # Example: df = pd.read_csv("nse_data.csv")
    data = {
        'Date': pd.date_range(start='2026-01-01', periods=10, freq='D'),
        'Ticker': ['SCOM', 'KCB', 'EQTY', 'SCOM', 'KCB', 'EQTY', 'SCOM', 'KCB', 'EQTY', 'SCOM'],
        'Price': [55.2, 30.1, 45.5, 56.0, 29.8, 46.2, 54.8, 30.5, 47.0, 55.5],
        'Volume': [1000, 500, 700, 1200, 450, 800, 1100, 600, 750, 1300]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Options")
ticker_list = df['Ticker'].unique()
selected_ticker = st.sidebar.multiselect("Select Stock(s)", ticker_list, default=ticker_list)

date_range = st.sidebar.date_input("Select Date Range", [])

# 4. Filter the Data
filtered_df = df[df['Ticker'].isin(selected_ticker)]

# 5. Visualizations
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Trends")
    fig_price = px.line(filtered_df, x='Date', y='Price', color='Ticker', markers=True)
    st.plotly_chart(fig_price, use_container_width=True)

with col2:
    st.subheader("Trading Volume")
    fig_vol = px.bar(filtered_df, x='Date', y='Volume', color='Ticker', barmode='group')
    st.plotly_chart(fig_vol, use_container_width=True)

# 6. Data Table
st.subheader("Raw Market Data")
st.dataframe(filtered_df, use_container_width=True)
