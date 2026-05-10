import yfinance as yf
from datetime import datetime

#define the holdings in the portfolio - ticker, units held, and average price paid
holdings = [
    {"ticker": "ASIA.AX", "units": 267.5603, "avg_price": 5047.80/267.5603},
    {"ticker": "IVV.AX", "units": 247.4956, "avg_price": 16749.99/247.4956},
    {"ticker": "VEU.AX", "units": 049.3132, "avg_price": 5684.11/49.3132},
]

old_holdings = [
    {"ticker": "ASIA.AX", "units": 114.0000, "avg_price": 1995/114},
    {"ticker": "IVV.AX", "units": 246.5587, "avg_price": 16092.90/246.5587},
    {"ticker": "VEU.AX", "units": 61.6686, "avg_price": 6944.03/61.6686},
]

#define a function to fetch all relevant yfinance data
def fetch_price_data(ticker):
    data = yf.Ticker(ticker)
    info = data.fast_info

    current_price = info["last_price"]
    previous_price = info["previous_close"]
    day_change = current_price - previous_price
    day_change_percent = (day_change / previous_price) * 100

    return {
        "current_price": current_price,
        "previous_price": previous_price,
        "day_change": day_change,
        "day_change_percent": day_change_percent,
    }

#define a function to build a list of dictionaries (one per holding)
def build_dashboard_rows():
    rows = []

    for holding in holdings:

        ticker = holding["ticker"]
        price_data = fetch_price_data(ticker)

        units = holding["units"]
        avg_price = holding["avg_price"]
        current_price = price_data["current_price"]
        day_change = price_data["day_change"] * units
        day_change_percent = price_data["day_change_percent"]

        total_invested = units * avg_price
        current_value = units * current_price
        total_return = current_value - total_invested
        total_return_percent = (total_return / total_invested) * 100

        rows.append({
            "ticker": ticker,
            "units": units,
            "avg_price": avg_price,
            "current_price": current_price,
            "day_change": day_change,
            "day_change_percent": day_change_percent,
            "current_value": current_value,
            "total_invested": total_invested,
            "total_return": total_return,
            "total_return_percent": total_return_percent,
        })


    # calculate total portfolio value and weight of each holding
    portfolio_value = sum(row["current_value"] for row in rows)

    #add weight to each holding's dictionary
    for row in rows:
        row["weight_percent"] = (row["current_value"] / portfolio_value) * 100

    return rows

#define helper functions to change text colour based on sign of value
def colour_value(value, text, width=None):
    if width != None:
        text = f"{text:>{width}}" #formats the text to be right aligned with a specified width
        
    if value > 0:
        return f"\033[92m{text}\033[0m"  # green for positive values
    elif value < 0:
        return f"\033[91m{text}\033[0m"  # red for negative values
    else:
        return text  # default colour for zero values

#define helper functions to format money and percentages in the dashboard
def format_money(value):
    return f"{value:,.2f}"


def format_signed_money(value, width=None):
    text = f"{value:+,.2f}"
    return colour_value(value, text, width)


def format_signed_percent(value, width=None):
    text = f"{value:+,.2f}"
    return colour_value(value, text, width)

def format_percent(value):
    return f"{value:,.2f}%"



#define function to print the dashboard to console
def print_dashboard(rows):
    #define the time the data was fetched to be printed at the top of the dashboard
    fetch_time = datetime.now().strftime("%I:%M:%S %p")

    #define portfolio level metrics to be printed at the top of the dashboard
    portfolio_value = sum(row["current_value"] for row in rows)
    total_invested = sum(row["total_invested"] for row in rows)
    portfolio_return = portfolio_value - total_invested
    portfolio_return_percent = (portfolio_return / total_invested) * 100
    portfolio_day_change = sum(row["day_change"] for row in rows)
    portfolio_day_change_percent = (portfolio_day_change / (portfolio_value - portfolio_day_change)) * 100

    print(f"Portfolio value: {format_money(portfolio_value)}")
    print(f"Total invested:  {format_money(total_invested)}")
    print(f"Portfolio return: {format_signed_money(portfolio_return)} ({format_signed_percent(portfolio_return_percent)})")
    print(f"Day change:      {format_signed_money(portfolio_day_change)} ({format_signed_percent(portfolio_day_change_percent)})")
    print() #prints a blank line to make the spacing nicer

    print(
        f"{'Ticker':>8}"
        f"{'Units':>11}"
        f"{'Avg Price':>12}"
        f"{'Current Price':>16}"
        f"{'Day Change':>14}"
        f"{'(%)':>9}"
        f"{'Invested':>14}"
        f"{'Value':>14}"
        f"{'Return':>12}"
        f"{'(%)':>9}"
        f"{'Weight':>10}"        
    )

    for row in rows:
        print(
            f"{row['ticker']:>8}"
            f"{row['units']:>11.4f}"
            f"{format_money(row['avg_price']):>12}"
            f"{format_money(row['current_price']):>16}"
            f"{format_signed_money(row['day_change'], width = 14)}"
            f"{format_signed_percent(row['day_change_percent'], width = 9)}"
            f"{format_money(row['total_invested']):>14}"
            f"{format_money(row['current_value']):>14}"
            f"{format_signed_money(row['total_return'], width = 12)}"
            f"{format_signed_percent(row['total_return_percent'], width = 9)}"
            f"{format_percent(row['weight_percent']):>10}"
        )

    print() #prints a blank line at the end of the dashboard for nicer spacing

    print(f"Last updated:    {fetch_time}")


if __name__ == "__main__":
    rows = build_dashboard_rows()
    print_dashboard(rows)
