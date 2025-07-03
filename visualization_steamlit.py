import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

st.set_page_config(layout="wide")

st.title("Nifty 50 Stock Analysis Dashboard")

@st.cache_data
def load_data():
    data_path = "processed_data/final_stock_data.csv"
    if not os.path.exists(data_path):
        st.error("Data file not found. Please generate it using the preprocessing script.")
        return None
    return pd.read_csv(data_path, parse_dates=["date"])

df = load_data()

if df is not None:
    st.sidebar.header("Filters")
    selected_stocks = st.sidebar.multiselect("Select Stock(s)", sorted(df["Ticker"].unique()), default=None)
    selected_months = st.sidebar.multiselect("Select Month(s)", sorted(df["month"].unique()), default=None)

    if selected_stocks:
        df = df[df["Ticker"].isin(selected_stocks)]
    if selected_months:
        df = df[df["month"].isin(selected_months)]

    st.subheader("1. Top 10 Most Volatile Stocks")
    df["daily_return"] = df.groupby("Ticker")["close"].pct_change()
    volatility = df.groupby("Ticker")["daily_return"].std().dropna().sort_values(ascending=False).head(10)
    fig_vol = px.bar(volatility, x=volatility.index, y=volatility.values, labels={"x": "Stock", "y": "Volatility"})
    st.plotly_chart(fig_vol, use_container_width=True) 

    st.subheader("2. Cumulative Return Over Time (Top 5)")
    df = df.sort_values(["Ticker", "date"])
    df["cumulative_return"] = df.groupby("Ticker")["daily_return"].transform(lambda x: (1 + x).cumprod())
    total_return = df.groupby("Ticker")["cumulative_return"].last().sort_values(ascending=False).head(5)
    top5 = df[df["Ticker"].isin(total_return.index)]
    fig_cum = px.line(top5, x="date", y="cumulative_return", color="Ticker")
    st.plotly_chart(fig_cum, use_container_width=True)

    st.subheader("3. Sector-wise Average Return")
    sector_map = pd.read_csv("processed_data/sector_mapping.csv")
    df = df.merge(sector_map, on="Ticker", how="left")
    yearly_return = df.groupby("Ticker")["cumulative_return"].last().reset_index()
    sector_df = yearly_return.merge(sector_map, on="Ticker")
    avg_sector_return = sector_df.groupby("Sector")["cumulative_return"].mean().sort_values(ascending=False)
    fig_sector = px.bar(avg_sector_return, x=avg_sector_return.index, y=avg_sector_return.values, labels={"x": "Sector", "y": "Average Return"})
    st.plotly_chart(fig_sector, use_container_width=True)

    st.subheader("4. Stock Price Correlation Heatmap")
    pivot_close = df.pivot_table(index="date", columns="Ticker", values="close")
    correlation = pivot_close.pct_change().corr()
    fig_corr, ax = plt.subplots(figsize=(14, 10))
    sns.heatmap(correlation, cmap="coolwarm", ax=ax)
    st.pyplot(fig_corr)

    st.subheader("5. Top 5 Monthly Gainers and Losers")
    df["monthly_return"] = df.groupby(["Ticker", "month"])["close"].transform(lambda x: x.iloc[-1] / x.iloc[0] - 1)
    months = sorted(df["month"].unique())
    for month in months:
        st.markdown(f"#### {month}")
        month_df = df[df["month"] == month]
        last_returns = month_df.groupby("Ticker")["monthly_return"].mean()
        gainers = last_returns.sort_values(ascending=False).head(5)
        losers = last_returns.sort_values().head(5)

        col1, col2 = st.columns(2)
        with col1:
            fig_gainers = px.bar(gainers, x=gainers.index, y=gainers.values, title="Top 5 Gainers")
            st.plotly_chart(fig_gainers, use_container_width=True)
        with col2:
            fig_losers = px.bar(losers, x=losers.index, y=losers.values, title="Top 5 Losers")
            st.plotly_chart(fig_losers, use_container_width=True)
else:
    st.warning("Data is not available. Please ensure preprocessing script has run.")
