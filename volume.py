import pandas as pd
import yfinance as yf
import plotly.graph_objects as go


def fetch_stock_data(ticker, start_date, end_date):
    # Fetch stock data using yfinance
    df = yf.download(ticker, start=start_date, end=end_date)
    return df


def plot_candlestick_bollinger(data):
    fig = go.Figure()

    # Candlestick trace
    fig.add_trace(
        go.Candlestick(
            x=data.index,
            open=data["Open"],
            high=data["High"],
            low=data["Low"],
            close=data["Close"],
            name="Candlesticks",
        )
    )

    # Bollinger Bands traces
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Bollinger_Bands_Upper"],
            name="Upper Bollinger Band",
            line=dict(color="red"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.index,
            y=data["Bollinger_Bands_Lower"],
            name="Lower Bollinger Band",
            line=dict(color="green"),
        )
    )

    fig.update_layout(
        title="TSLA Stock Prices with Bollinger Bands",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
    )

    return fig


def plot_volume(data):
    fig = go.Figure()

    # Color volume bars based on up or down day
    colors = [
        "green" if data["Close"].iloc[i] >= data["Close"].iloc[i - 1] else "red"
        for i in range(1, len(data))
    ]

    # Volume bar trace
    fig.add_trace(
        go.Bar(
            x=data.index[1:], y=data["Volume"][1:], marker_color=colors, name="Volume"
        )
    )

    fig.update_layout(
        # title="TSLA Stock Volume",
        # xaxis_title="Date",
        yaxis_title="Volume",
        xaxis_rangeslider_visible=False,
    )
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(height=300)

    return fig


if __name__ == "__main__":
    # Define the stock symbol (TSLA for Tesla)
    stock_symbol = "TSLA"

    # Define the date range for one year
    start_date = "2022-01-01"
    end_date = "2023-01-01"

    # Fetch TSLA stock data
    tsla_data = fetch_stock_data(stock_symbol, start_date, end_date)

    # Calculate Bollinger Bands
    window = 20
    tsla_data["Rolling_Mean"] = tsla_data["Close"].rolling(window=window).mean()
    tsla_data["Bollinger_Bands_Upper"] = (
        tsla_data["Rolling_Mean"] + 2 * tsla_data["Close"].rolling(window=window).std()
    )
    tsla_data["Bollinger_Bands_Lower"] = (
        tsla_data["Rolling_Mean"] - 2 * tsla_data["Close"].rolling(window=window).std()
    )

    # Plot candlestick with Bollinger Bands
    candlestick_bollinger_fig = plot_candlestick_bollinger(tsla_data)
    # candlestick_bollinger_fig.show()
    # Plot volume
    volume_fig = plot_volume(tsla_data)
    volume_fig.show()

    # Combine both figures on the same timeline
    # combined_fig = go.Figure(candlestick_bollinger_fig.data + volume_fig.data)
    # combined_fig.update_layout(height=800)

    # combined_fig.show()
