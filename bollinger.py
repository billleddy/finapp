import yfinance as yf
import plotly.graph_objects as go


def plot_candle_chart_with_bollinger_bands(
    ticker_symbol, start_date, end_date, window_size=20, num_std_dev=2
):
    # Fetch historical stock data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # Calculate moving average and standard deviation
    stock_data["MA"] = stock_data["Close"].rolling(window=window_size).mean()
    stock_data["Upper"] = stock_data["MA"] + (
        stock_data["Close"].rolling(window=window_size).std() * num_std_dev
    )
    stock_data["Lower"] = stock_data["MA"] - (
        stock_data["Close"].rolling(window=window_size).std() * num_std_dev
    )

    # Create candlestick chart with Bollinger Bands
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=stock_data.index,
                open=stock_data["Open"],
                high=stock_data["High"],
                low=stock_data["Low"],
                close=stock_data["Close"],
                name="Candlesticks",
            ),
            go.Scatter(
                x=stock_data.index,
                y=stock_data["Upper"],
                mode="lines",
                line=dict(color="red"),
                name="Upper Band",
            ),
            go.Scatter(
                x=stock_data.index,
                y=stock_data["MA"],
                mode="lines",
                line=dict(color="black"),
                name="Moving Average",
            ),
            go.Scatter(
                x=stock_data.index,
                y=stock_data["Lower"],
                mode="lines",
                line=dict(color="blue"),
                name="Lower Band",
            ),
        ]
    )

    # Customize the chart layout
    fig.update_layout(
        title=f"{ticker_symbol} Stock Price with Bollinger Bands",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
    )

    # Show the chart
    fig.show()


# Set the ticker symbol, start date, and end date
symbol = "IBM"
start_date = "2022-01-01"
end_date = "2024-01-01"

# Plot the candlestick chart with Bollinger Bands
plot_candle_chart_with_bollinger_bands(symbol, start_date, end_date)
