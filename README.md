# ETF Dashboard

A personal ETF portfolio tracker for Australian-listed ETFs.

The project pulls live price data from Yahoo Finance, calculates portfolio value, daily movement, total return, and portfolio weights, then displays the results in either a Streamlit dashboard, a macOS menu bar widget, or the terminal.

## Files

- `tracker.py`: Stores holdings, fetches prices, calculates returns, and can print the tracker in the terminal.
- `app.py`: Streamlit dashboard with portfolio metrics and a holdings table.
- `widget.py`: macOS menu bar widget with refresh, quit, and full-dashboard options.
- `icon.png`: App icon image.
- `ETF Widget.app/`: Automator app bundle used to launch the widget.

## Setup

Create and activate a virtual environment:

```zsh
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```zsh
pip install streamlit pandas yfinance rumps pyobjc
```

## Run The Dashboard

```zsh
source .venv/bin/activate
streamlit run app.py
```

## Run The Menu Bar Widget

```zsh
source .venv/bin/activate
python widget.py
```

## Run The Terminal Version

```zsh
source .venv/bin/activate
python tracker.py
```

## Editing Holdings

Update the `holdings` list in `tracker.py`.

Example:

```python
holdings = [
    {"ticker": "ASIA.AX", "units": 267.5603, "avg_price": 5047.80 / 267.5603},
    {"ticker": "IVV.AX", "units": 247.4956, "avg_price": 16749.99 / 247.4956},
    {"ticker": "VEU.AX", "units": 49.3132, "avg_price": 5684.11 / 49.3132},
]
```

Use Yahoo Finance ticker symbols. Australian ETFs usually end in `.AX`.

## Notes

This project depends on Yahoo Finance data through `yfinance`, so price fetching can fail if Yahoo is unavailable, the network is down, or a ticker cannot be resolved.

This dashboard is for personal tracking and learning only. It is not financial advice.
