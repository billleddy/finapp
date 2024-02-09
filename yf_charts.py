import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
from dateutil import relativedelta
import talib
import pandas as pd
import matplotlib.pyplot as plt
import os

narration = {}  # narration slide type


# Plot the 50 and 200 day moving averages
def moving_averages(ticker_symbol, days, data):
    fig = go.Figure()

    # Plot 50-day moving average
    fifty = data["Close"].rolling(window=50).mean()
    fig.add_trace(
        go.Scatter(
            x=data.tail(days).index,
            y=fifty.tail(days),  # data["Close"].rolling(window=50).mean(),
            mode="lines",
            name="50-day MA",
        )
    )

    # Plot 200-day moving average
    fig.add_trace(
        go.Scatter(
            x=data.tail(days).index,
            y=data["Close"].rolling(window=200).mean().tail(days),
            mode="lines",
            name="200-day MA",
        )
    )

    # Plot stock prices
    fig.add_trace(
        go.Scatter(
            x=data.tail(days).index,
            y=data["Close"].tail(days),
            mode="lines",
            name="Stock Price",
        )
    )

    fig.update_layout(
        title=f"{ticker_symbol} 50 & 200 Day Moving Averages",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
        paper_bgcolor="black",
        plot_bgcolor="black",
    )

    # Save the chart
    filename = f"{ticker_symbol}/{days}_ma.png"
    fig.write_image(filename)  # fig.show()


def calculate_rsi(data):
    # Calculate RSI
    data["rsi"] = talib.RSI(data["Close"], timeperiod=14)
    return data


def rsi(ticker_symbol, days, stock_data):
    data = calculate_rsi(data=stock_data)
    fig = go.Figure()

    # Plot RSI
    fig.add_trace(
        go.Scatter(
            x=data.tail(days).index,
            y=data["rsi"].tail(days),
            mode="lines",
            name="RSI",
            line=dict(color="cyan"),
        )
    )

    # Add horizontal lines for overbought and oversold levels
    fig.add_shape(
        dict(
            type="line",
            x0=data.tail(days).index.min(),
            x1=data.tail(days).index.max(),
            y0=70,
            y1=70,
            line=dict(color="fuchsia"),
            name="Overbought",
        )
    )
    fig.add_shape(
        dict(
            type="line",
            x0=data.tail(days).index.min(),
            x1=data.tail(days).index.max(),
            y0=30,
            y1=30,
            line=dict(color="chartreuse"),
            name="Oversold",
        )
    )

    fig.update_layout(
        title=f"{ticker_symbol} Relative Strength Indicator",  # xaxis_title="Date",
        yaxis_title="RSI",
        xaxis_rangeslider_visible=False,
        paper_bgcolor="black",
        plot_bgcolor="black",
    )

    # Save the chart
    filename = f"{ticker_symbol}/{days}_rsi.png"
    fig.write_image(filename)  # fig.show()


def calculate_macd(stock_data):
    # Calculate MACD
    stock_data["macd"], stock_data["signal"], _ = talib.MACD(
        stock_data["Close"], fastperiod=12, slowperiod=26, signalperiod=9
    )
    return stock_data


def macd(ticker_symbol, days, stock_data):
    data = calculate_macd(stock_data)

    fig = go.Figure()

    # Plot MACD and Signal lines
    fig.add_trace(
        go.Scatter(
            x=data.tail(days).index,
            y=data["macd"].tail(days),
            mode="lines",
            name="MACD",
            line=dict(color="chartreuse"),
        )
    )
    fig.add_trace(
        go.Scatter(
            x=data.tail(days).index,
            y=data["signal"].tail(days),
            mode="lines",
            name="Signal",
            line=dict(color="fuchsia"),
        )
    )

    # Plot histogram for MACD
    fig.add_trace(
        go.Bar(
            x=data.tail(days).index,
            y=data["macd"].tail(days) - data["signal"].tail(days),
            name="MACD Histogram",
            marker=dict(color="blue"),
        )
    )

    fig.update_layout(
        title=f"{ticker_symbol} Moving Average Convergence/Divergence",
        # xaxis_title="Date",
        yaxis_title="MACD",
        xaxis_rangeslider_visible=False,
        paper_bgcolor="black",
        plot_bgcolor="black",
    )

    # Save the chart
    filename = f"{ticker_symbol}/{days}_macd.png"
    fig.write_image(filename)  # fig.show()


def bollinger_candle(ticker_symbol, days, stock_data, window_size=20, num_std_dev=2):
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
                x=stock_data.tail(days).index,
                open=stock_data["Open"].tail(days),
                high=stock_data["High"].tail(days),
                low=stock_data["Low"].tail(days),
                close=stock_data["Close"].tail(days),
                name="Candlesticks",
                showlegend=False,
                increasing=dict(line=dict(color="chartreuse")),
                decreasing=dict(line=dict(color="red")),
            ),
            go.Scatter(
                x=stock_data.tail(days).index,
                y=stock_data["Upper"].tail(days),
                mode="lines",
                line=dict(color="fuchsia"),
                name="Upper Band",
                showlegend=False,
            ),
            go.Scatter(
                x=stock_data.tail(days).index,
                y=stock_data["MA"].tail(days),
                mode="lines",
                line=dict(color="white"),
                name="Moving Average",
                showlegend=False,
            ),
            go.Scatter(
                x=stock_data.tail(days).index,
                y=stock_data["Lower"].tail(days),
                mode="lines",
                line=dict(color="greenyellow"),
                name="Lower Band",
                showlegend=False,
            ),
        ],
        rows=[1, 1, 1, 1],
        cols=[1, 1, 1, 1],
    )

    # Color volume bars based on up or down day
    subset = stock_data.tail(days)
    colors = [
        (
            "chartreuse"
            if subset["Close"].iloc[i] >= subset["Close"].iloc[i - 1]
            else "red"
        )
        for i in range(1, len(subset))
    ]

    # Volume bar trace
    fig.add_trace(
        go.Bar(
            x=stock_data.tail(days).index[1:],
            y=stock_data.tail(days)["Volume"][1:],
            marker_color=colors,
            name="Volume",
            showlegend=False,
        ),
        row=2,
        col=1,
    )

    # Customize the chart layout
    fig.update_layout(
        title=f"{ticker_symbol} Stock Price with Bollinger Bands",
        # xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="lavender"),
    )

    # Save the chart
    filename = f"{ticker_symbol}/{days}_bollinger.png"
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
            showlegend=False,
            increasing=dict(line=dict(color="chartreuse")),
            decreasing=dict(line=dict(color="red")),
        ),
        row=1,
        col=1,
    )
    # Color volume bars based on up or down day
    colors = [
        (
            "chartreuse"
            if stock_data["Close"].iloc[i] >= stock_data["Close"].iloc[i - 1]
            else "red"
        )
        for i in range(1, len(stock_data))
    ]

    fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="lavender"),
    )

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
        title=f"{ticker_symbol} {period} Stock Price Chart",
        # xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
    )

    # Save the chart
    filename = ticker_symbol + "/" + period + "_candle.png"
    fig.write_image(filename)  # fig.show()


def volume(ticker_symbol, period, stock_data):
    fig = go.Figure()

    # Color volume bars based on up or down day
    colors = [
        "green" if stock_data["Close"].iloc[i] >= stock_data["Open"].iloc[i] else "red"
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


def news(ticker_symbol, yf_stock):
    news = yf_stock.news
    headlines = ""
    i = 1
    for n in news:
        title = n["title"]
        publisher = n["publisher"]
        when = datetime.fromtimestamp(n["providerPublishTime"])
        date_str = when.strftime("%H:%M %m/%d/%Y")
        headlines += f"{title}\nPause:0.5\n"

        narration[f"Headline{i}"] = f"'{title}' - {publisher} @ {date_str} GMT "
        i += 1
    narration["Headlines"] = headlines


def plot_dataframe(ticker_symbol, df, x_column, y_column, title="Graph"):
    # Convert the 'date' column to datetime if it's not already
    if pd.api.types.is_datetime64_any_dtype(df[x_column]):
        df[x_column] = pd.to_datetime(df[x_column])

    # Sort the DataFrame by the 'date' column
    df = df.sort_values(by=x_column)

    # Plot the graph
    plt.figure(figsize=(10, 6))
    # plt.plot(df[x_column], df[y_column], marker=",", linestyle="solid", color="r")
    plt.bar(df[x_column], df[y_column].div(1000), color="red", width=2.0)

    # Customize the plot
    plt.title(title)
    # plt.xlabel("Time")
    plt.ylabel("Shares(1000s)")
    plt.grid(True)
    # plt.show()

    # Save the chart
    filename = ticker_symbol + "/insider.png"
    plt.savefig(filename)


# https://pypi.org/project/yfinance/
def insider(ticker_symbol, yf_stock):
    df = yf_stock.insider_transactions
    # Call the function to plot the graph
    plot_dataframe(
        ticker_symbol,
        df,
        x_column="Start Date",
        y_column="Shares",
        title="Insider Selling",
    )


def up_downgrades(ticker_symbol, yf_stock):
    df = yf_stock.upgrades_downgrades
    cell_color = "black"
    head_rows = df.head(12)  # df could be very long we only want the latest
    plt.rcParams["text.color"] = "white"
    plt.figure(figsize=(6, 3.0))
    fig = plt.gcf()

    # Set the background color
    fig.set_facecolor("black")
    fig.set_edgecolor("blue")

    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    table_data = []
    cell_colors = []
    for i, (index, row) in enumerate(head_rows.iterrows()):
        if row["Action"] == "down":
            action_color = "red"
        elif row["Action"] == "up":
            action_color = "#7fff7f"  # "green"
        else:
            action_color = cell_color

        if row["ToGrade"] == "Sell":
            grade_color = "red"
        elif row["ToGrade"] == "Outperform":
            grade_color = "#7fff7f"  # "green"
        elif row["ToGrade"] == "Underweight":
            grade_color = "yellow"
        else:
            grade_color = cell_color
        cell_colors.append(
            [cell_color, cell_color, grade_color, cell_color, action_color]
        )

        table_data.append(
            [
                index.strftime("%Y-%m-%d"),
                row["Firm"],
                row["ToGrade"],
                row["FromGrade"],
                row["Action"],
            ]
        )

    colLabels = ["Date", "Firm", "New Grade", "Prev Grade", "Action"]
    table = plt.table(
        cellText=table_data,
        colLabels=colLabels,  # head_rows.columns,
        cellLoc="center",
        loc="center",
        colColours=[cell_color] * len(colLabels),
        # cellColours=[["#f0f0f0", "#f0f0f0", "#f0f0f0", "#f0f0f0", "#f0f0f0"]]
        cellColours=cell_colors,
        # colWidth=[0.2, 0.2, 0.2, 0.2],
    )

    for i, cell in enumerate(table.get_celld().values()):
        c = i % len(colLabels)
        r = int(i / len(colLabels))
        if r >= len(cell_colors):
            break
        colors = cell_colors[r]
        if colors[c] != "black":
            # highlighted cell
            cell.set_text_props(color="black")  # fontweight="bold",
        else:
            cell.set_text_props(color="white")

    plt.savefig(f"{ticker_symbol}/up_down.png", bbox_inches="tight", pad_inches=0.05)


# msft.recommendations
# msft.recommendations_summary
# msft.upgrades_downgrades


# turn "0m,-3m,-6m,-9m" into Nov, Aug...
def get_month(delta):
    months = 0
    if delta.find("1") >= 0:
        months = 1
    elif delta.find("2") >= 0:
        months = 2
    elif delta.find("3") >= 0:
        months = 3

    then = datetime.now() - relativedelta.relativedelta(months=months)

    # Get the three-letter name of the month
    month_name = then.strftime("%b")
    return month_name


def recommendations(ticker_symbol, yf_stock):
    df = yf_stock.recommendations  # same as recommendations_summary?
    plt.figure(figsize=(6, 1.5))
    fig = plt.gcf()

    # Set the background color
    fig.set_facecolor("#37474f")

    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # modify the period to show the month
    df["when"] = df["period"].apply(get_month)

    table_data = []
    for i, (index, row) in enumerate(df.iterrows()):
        table_data.append(
            [
                row["when"],
                row["strongBuy"],
                row["buy"],
                row["hold"],
                row["sell"],
                row["strongSell"],
            ]
        )

    colLabels = ["When", "Strong Buy", "Buy", "Hold", "Sell", "Strong Sell"]
    table = plt.table(
        cellText=table_data,
        colLabels=colLabels,  # head_rows.columns,
        cellLoc="center",
        loc="center",
        colColours=["#f0f0f0"] * len(colLabels),
        cellColours=[["#f0f0f0", "#f0f0f0", "#f0f0f0", "#f0f0f0", "#f0f0f0", "#f0f0f0"]]
        * len(df),
    )

    plt.savefig(
        f"{ticker_symbol}/recommendations.png", bbox_inches="tight", pad_inches=0.05
    )


def format_date_with_suffix(date):
    day = date.day
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return date.strftime(f"%B {day}{suffix}")  # , %Y")


def dollars_to_words(val):
    rv = ""
    if val >= 1:
        v = int(val)
        if v == 1:
            rv += "one dollar and "
        else:
            rv += f"{v} dollars and "
    cents = int((val * 100) % 100)
    if cents == 1:
        rv += "one cent"
    else:
        rv += f"{cents} cents"
    return rv


def earnings(ticker_symbol, yf_stock):
    df = yf_stock.earnings_dates
    plt.figure(figsize=(6, 2.3))
    fig = plt.gcf()

    # Set the background color
    fig.set_facecolor("#37474f")

    ax = plt.subplot(111, frame_on=False)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)

    # remove future EPS dates that have Reported = NaN
    # find the first row with an Estimate
    # Find the index of the first non-NaN value in the specified column
    date = df["EPS Estimate"].first_valid_index()
    earnings_day = format_date_with_suffix(date)
    estval = df.at[date, "EPS Estimate"]  # TODO handle dollars
    estimate = dollars_to_words(estval)
    narration["next_EPS"] = "Next: " + date.strftime("%m/%d/%y")
    narration["EPS"] = (
        f"Next earnings will report on {earnings_day} with a current estimate of {estimate}. "
    )
    df_rows = df.dropna(subset=["Reported EPS"])
    table_data = []
    cell_colors = []
    for i, (index, row) in enumerate(df_rows.iterrows()):
        if row["Surprise(%)"] < -0.01:
            surprise_color = "red"
        elif row["Surprise(%)"] > 0.1:
            surprise_color = "#7fff7f"  # "green"
        else:
            surprise_color = "#f0f0f0"

        cell_colors.append(["#f0f0f0", "#f0f0f0", "#f0f0f0", surprise_color])
        table_data.append(
            [
                index.strftime("%Y-%m-%d"),
                row["EPS Estimate"],
                row["Reported EPS"],
                row["Surprise(%)"],
            ]
        )

    colLabels = ["Date", "Estimate", "Reported", "Surprise(%)"]
    table = plt.table(
        cellText=table_data,
        colLabels=colLabels,
        cellLoc="center",
        loc="center",
        colColours=["#f0f0f0"] * len(colLabels),
        cellColours=cell_colors,
    )

    plt.savefig(f"{ticker_symbol}/earnings.png", bbox_inches="tight", pad_inches=0.05)


def options(ticker_symbol, yf_stock):
    print("Options does not seem to return anything so don't call this function")


def default_narration(company, ticker_symbol, today_date):
    narration["summary"] = (
        "So is it time to buy or hold or sell {company}?\nPause:0.75\nOr maybe just run away?"
    )


def get_charts(ticker_symbol, start_date, end_date):
    os.makedirs(ticker_symbol, exist_ok=True)
    yf_stock = yf.Ticker(ticker_symbol)

    # Fetch historical stock data
    stock_data = yf.download(ticker_symbol, start=start_date, end=end_date)

    # test
    up_downgrades(ticker_symbol, yf_stock)
    exit(0)
    # test

    # Candle 5 year
    candle(ticker_symbol=ticker_symbol, period="5 Year", stock_data=stock_data)
    exit(0)
    moving_averages(ticker_symbol=ticker_symbol, days=365, data=stock_data)

    # Candle 90 days
    ninety = stock_data.tail(90).copy()
    candle(ticker_symbol=ticker_symbol, period="90 Day", stock_data=ninety)
    rsi(ticker_symbol=ticker_symbol, days=90, stock_data=stock_data)
    macd(ticker_symbol=ticker_symbol, days=90, stock_data=stock_data)

    # Bollinger & Candle 90 days
    bollinger_candle(ticker_symbol=ticker_symbol, days=90, stock_data=stock_data)

    # Candle 5 days
    # TODO - missing first day of volume because its color is based on prev day
    five_day = stock_data.tail(5)
    candle(ticker_symbol=ticker_symbol, period="5 Day", stock_data=five_day)

    options(ticker_symbol, yf_stock)
    earnings(ticker_symbol, yf_stock)
    recommendations(ticker_symbol, yf_stock)
    up_downgrades(ticker_symbol, yf_stock)
    insider(ticker_symbol, yf_stock)
    news(ticker_symbol, yf_stock)


def main():
    # Set the ticker symbol, start date, and end date
    symbol = "TSLA"
    company = "Tesla"

    today_date = datetime.now().date()
    five_years = (datetime.now() - timedelta(days=365 * 5)).date()

    # Initialize the relatively static narration
    default_narration(company, symbol, today_date)
    # Plot the candlestick chart
    get_charts(symbol, five_years, today_date)


if __name__ == "__main__":
    main()
