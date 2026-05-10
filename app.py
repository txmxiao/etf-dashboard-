import pandas as pd
import streamlit as st
from datetime import datetime

from tracker import build_dashboard_rows, format_money
from widget import format_signed_money, format_signed_percent

# Set up Streamlit page configuration
st.set_page_config(page_title="ETF Widget", layout="wide")

st.title("Portfolio Tracker")

try: 
    rows = build_dashboard_rows()
except Exception as error:
    st.error("Could not fetch Yahoo data, try refreshing later.")
    st.caption(f"Error: {type(error).__name__}")
    st.stop()

# Create a dataframe from the rows
df = pd.DataFrame(rows)

portfolio_value = df["current_value"].sum()
total_invested = df["total_invested"].sum()
portfolio_return = portfolio_value - total_invested
portfolio_return_percent = (portfolio_return / total_invested) * 100
portfolio_day_change = df["day_change"].sum()
portfolio_day_change_percent = (portfolio_day_change / (portfolio_value - portfolio_day_change)) * 100

# Create top row of metrics to show total portfolio value, total invested and total return
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Portfolio Value", f"${format_money(portfolio_value)}")
col2.metric("Total Invested", f"${format_money(total_invested)}")
col3.metric("Day Change", f"{format_signed_money(portfolio_day_change)}", f"{format_signed_percent(portfolio_day_change_percent)}")
col4.metric("Portfolio Return", f"{format_signed_money(portfolio_return)}", f"{format_signed_percent(portfolio_return_percent)}")

# Create a dataframe to display the individual ETF holdings with the relevant metrics
display_df = df[
[
    "ticker",
    "units",
    "avg_price",
    "current_price",
    "day_change",
    "day_change_percent",
    "total_invested",
    "current_value",
    "total_return",
    "total_return_percent",
    "weight_percent",

    ]
]

# Define function to colour positive values green and negative values red
def colour_positive_negative(value):
    if value > 0:
        return "color: #22c55e"
    elif value < 0:
        return "color: #ef4444"
    else:
        return ""

# Apply formatting to the dataframe and colour the relevant columns based on positive or negative values
styled_df = display_df.style.format(
    {
        "units": "{:,.4f}",
        "avg_price": "{:,.2f}",
        "current_price": "{:,.2f}",
        "day_change": "{:+.2f}",
        "day_change_percent": "{:+.2f}%",
        "total_invested": "{:,.2f}",
        "current_value": "{:,.2f}",
        "total_return": "{:+.2f}",
        "total_return_percent": "{:+.2f}%",
        "weight_percent": "{:.2f}%",
    }
).map(
    colour_positive_negative,
    subset=["day_change", "day_change_percent", "total_return", "total_return_percent"],
)

st.write("") #add a blank line for spacing 


# Display the styled dataframe in Streamlit with appropriate column configurations
st.dataframe(
    styled_df,
    column_config={
        "ticker": st.column_config.TextColumn("Ticker", width = 60),
        "units": st.column_config.NumberColumn("            Units", width = 60),
        "avg_price": st.column_config.NumberColumn("    Avg Price", width = 60),
        "current_price": st.column_config.NumberColumn("       Live Price", width = 70),
        "day_change": st.column_config.NumberColumn("  Day Change", width = 70),
        "day_change_percent": st.column_config.NumberColumn("             (%)", width = 50),
        "total_invested": st.column_config.NumberColumn("  Total Invested", width = 80),
        "current_value": st.column_config.NumberColumn("    Total Value", width = 70),
        "total_return": st.column_config.NumberColumn("  Total Return", width = 70),
        "total_return_percent": st.column_config.NumberColumn("             (%)", width = 50),
        "weight_percent": st.column_config.NumberColumn("        Weight", width = 50),
    },
    hide_index=True,
)


last_updated = datetime.now().strftime("%I:%M:%S %p")
st.caption(f"Last updated: {last_updated}")#add a blank caption to create some spacing

st.write("") #add a blank line for spacing

st.caption("Press 'R' to refresh")
