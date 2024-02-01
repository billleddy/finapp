import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from datetime import datetime, timedelta

# data
# df = pd.read_csv(
#    "https://raw.githubusercontent.com/plotly/datasets/master/finance-charts-apple.csv"
# )
ticker_symbol = "TSLA"

end_date = datetime.now().date()
start_date = (datetime.now() - timedelta(days=365 * 5)).date()
df = yf.download(ticker_symbol, start=start_date, end=end_date)

# Create subplots and mention plot grid size
fig = make_subplots(
    rows=2,
    cols=1,
    shared_xaxes=True,
    vertical_spacing=0.03,
    subplot_titles=("OHLC", "Volume"),
    row_width=[0.2, 0.7],
)

# Plot OHLC on 1st row
fig.add_trace(
    go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="OHLC",
        showlegend=False,
    ),
    row=1,
    col=1,
)

# Bar trace for volumes on 2nd row without legend
fig.add_trace(
    go.Bar(x=df.index[1:], y=df["Volume"][1:], showlegend=False), row=2, col=1
)

# Do not show OHLC's rangeslider plot
fig.update(layout_xaxis_rangeslider_visible=False)
fig.show()
