import yfinance as yf
import plotly.graph_objects as go
from flask import Flask, render_template

app = Flask(__name__)


def get_candle_chart_data(
    ticker_symbol, start_date, end_date, window_size=20, num_std_dev=2
):
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)
    stock_data["MA"] = stock_data["Close"].rolling(window=window_size).mean()
    stock_data["Upper"] = stock_data["MA"] + (
        stock_data["Close"].rolling(window=window_size).std() * num_std_dev
    )
    stock_data["Lower"] = stock_data["MA"] - (
        stock_data["Close"].rolling(window=window_size).std() * num_std_dev
    )

    candlestick = go.Candlestick(
        x=stock_data.index,
        open=stock_data["Open"],
        high=stock_data["High"],
        low=stock_data["Low"],
        close=stock_data["Close"],
        name="Candlesticks",
    )

    upper_band = go.Scatter(
        x=stock_data.index,
        y=stock_data["Upper"],
        mode="lines",
        line=dict(color="red"),
        name="Upper Band",
    )
    moving_average = go.Scatter(
        x=stock_data.index,
        y=stock_data["MA"],
        mode="lines",
        line=dict(color="black"),
        name="Moving Average",
    )
    lower_band = go.Scatter(
        x=stock_data.index,
        y=stock_data["Lower"],
        mode="lines",
        line=dict(color="blue"),
        name="Lower Band",
    )

    return [candlestick, upper_band, moving_average, lower_band]


@app.route("/")
def index():
    # Set the ticker symbol, start date, and end date
    symbol = "IBM"
    start_date = "2022-01-01"
    end_date = "2024-01-01"

    # Get candlestick chart data
    chart_data = get_candle_chart_data(symbol, start_date, end_date)

    # Create layout
    layout = dict(
        title=f"{symbol} Stock Price with Bollinger Bands",
        xaxis=dict(title="Date"),
        yaxis=dict(title="Stock Price (USD)"),
        xaxis_rangeslider_visible=False,
    )

    # Create the figure
    fig = go.Figure(data=chart_data, layout=layout)

    # Return the HTML representation of the plot
    return render_template("plot.html", plot_html=fig.to_html())


if __name__ == "__main__":
    app.run(port=5001, debug=True)
