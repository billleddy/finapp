import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta


def bollinger_candle(ticker_symbol, period, stock_data, window_size=20, num_std_dev=2):
    # Calculate moving average and standard deviation
    stock_data["MA"] = stock_data["Close"].rolling(window=window_size).mean()
    stock_data["Upper"] = stock_data["MA"] + (
        stock_data["Close"].rolling(window=window_size).std() * num_std_dev
    )
    stock_data["Lower"] = stock_data["MA"] - (
        stock_data["Close"].rolling(window=window_size).std() * num_std_dev
    )
    # Create subplots and mention plot grid size
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(ticker_symbol, "Volume"),
        row_width=[0.2, 0.7],
    )

    # Create candlestick chart with Bollinger Bands
    fig.add_traces(
        [
            go.Candlestick(
                x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
                name="Candlesticks",
                showlegend=False,
            ),
            go.Scatter(
                x=stock_data.index,
                y=stock_data["Upper"],
                mode="lines",
                line=dict(color="red"),
                name="Upper Band",
                showlegend=False,
            ),
            go.Scatter(
                x=stock_data.index,
                y=stock_data["MA"],
                mode="lines",
                line=dict(color="black"),
                name="Moving Average",
                showlegend=False,
            ),
            go.Scatter(
                x=stock_data.index,
                y=stock_data["Lower"],
                mode="lines",
                line=dict(color="blue"),
                name="Lower Band",
                showlegend=False,
            ),
        ],
        rows=[1, 1, 1, 1],
        cols=[1, 1, 1, 1],
    )

    # Color volume bars based on up or down day
    colors = [
        "green"
        if stock_data["Close"].iloc[i] >= stock_data["Close"].iloc[i - 1]
        else "red"
        for i in range(1, len(stock_data))
    ]

    # Volume bar trace
    fig.add_trace(
        go.Bar(
            x=stock_data.index[1:],
            y=stock_data["Volume"][1:],
            marker_color=colors,
            name="Volume",
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    # Customize the chart layout
    fig.update_layout(
        title=f"{ticker_symbol} {period} Stock Price with Bollinger Bands",
        # xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
    )

    # Save the chart
    filename = ticker_symbol + "_" + period + "_bollinger.png"
    fig.write_image(filename)


def candle(ticker_symbol, period, stock_data):
    # Create subplots and mention plot grid size
    fig = make_subplots(
        rows=2,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        subplot_titles=(ticker_symbol, "Volume"),
        row_width=[0.2, 0.7],
    )

    fig.add_trace(
        go.Candlestick(
            x=stock_data.index,
            open=stock_data["Open"],
            high=stock_data["High"],
            low=stock_data["Low"],
            close=stock_data["Close"],
        ),
        row=1,
        col=1,
    )

    # Color volume bars based on up or down day
    colors = [
        "green"
        if stock_data["Close"].iloc[i] >= stock_data["Close"].iloc[i - 1]
        else "red"
        for i in range(1, len(stock_data))
    ]

    # Volume bar trace
    fig.add_trace(
        go.Bar(
            x=stock_data.index[1:],
            y=stock_data["Volume"][1:],
            marker_color=colors,
            name="Volume",
        ),
        row=2,
        col=1,
    )

    # Customize the chart layout
    fig.update_layout(
        title=f"{ticker_symbol} {period} Stock Price Chart",
        # xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
    )

    # Save the chart
    filename = ticker_symbol + "_" + period + "_candle.png"
    fig.write_image(filename)  # fig.show()


def volume(ticker_symbol, period, stock_data):
    fig = go.Figure()

    # Color volume bars based on up or down day
    colors = [
        "green"
        if stock_data["Close"].iloc[i] >= stock_data["Close"].iloc[i - 1]
        else "red"
        for i in range(1, len(stock_data))
    ]

    # Volume bar trace
    fig.add_trace(
        go.Bar(
            x=stock_data.index[1:],
            y=stock_data["Volume"][1:],
            marker_color=colors,
            name="Volume",
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

    # Save the chart
    # filename = ticker_symbol + "_" + period + "_volume.png"
    # fig.write_image(filename)  # fig.show()
    return fig


def get_charts(ticker_symbol, start_date, end_date):
    # Fetch historical stock data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Candle 5 year
    candle(ticker_symbol=ticker_symbol, period="5 Year", stock_data=stock_data)
    # volume(ticker_symbol=ticker_symbol, period="5 Year", stock_data=stock_data)

    # Candle 90 days
    ninety = stock_data.tail(90).copy()
    candle(ticker_symbol=ticker_symbol, period="90 Day", stock_data=ninety)
    # volume(ticker_symbol=ticker_symbol, period="90 Day", stock_data=ninety)

    # Bollinger & Candle 90 days
    bollinger_candle(ticker_symbol=ticker_symbol, period="90 Day", stock_data=ninety)

    # Candle 5 days
    five_day = stock_data.tail(90)
    candle(ticker_symbol=ticker_symbol, period="5 Day", stock_data=five_day)
    # volume(ticker_symbol=ticker_symbol, period="5 Day", stock_data=five_day)


# Set the ticker symbol, start date, and end date
symbol = "TSLA"

today_date = datetime.now().date()
five_years = (datetime.now() - timedelta(days=365 * 5)).date()

# Plot the candlestick chart
get_charts(symbol, five_years, today_date)
