import plotly.graph_objects as go
from datetime import datetime, timedelta

def plot_maGraph(maData, days_window, source):
    dates = [i["Date"] for i in maData]
    prices = [i["Close/Last"] for i in maData]
    sma = [i["SMA"] for i in maData]
    ema = [i["EMA"] for i in maData]
    # -------------------------------------------
    # 1. Create line plots for Close/Last and SMA
    # -------------------------------------------
    fig = go.Figure(
    data=[
        go.Scatter(
            x=dates,
            y=prices,
            mode='lines',
            name='Close Price'
        ),
        go.Scatter(
            x=dates,
            y=sma,
            mode='lines',
            name=f"{days_window}-day SMA"
        ),
        go.Scatter(
            x=dates,
            y=ema,
            mode='lines',
            name=f"{days_window}-day EMA"
        )
    ],
    # -------------------------------------------
    # 1.5 Customize layout of the graph with hover over interaction, namings, and information
    # -------------------------------------------
    layout=go.Layout(
        title_text=f"Daily Closing Price vs SMA vs EMA for {source}",
        hovermode='x unified',
        xaxis=dict(
            title_text='Date',
            unifiedhovertitle=dict(
                text='<b>%{x|%A, %B %d, %Y}</b>'
            )
        ),
        yaxis=dict(
            title_text='Price (USD)',
            tickprefix='$'
        )
    )
)
    # -------------------------------------------
    # 2. Show the graph
    # -------------------------------------------
    return fig.to_html(full_html = False)


def plot_indexGraph(stockData, source, date_filter):
    dates = stockData["Date"]
    prices = stockData["Close/Last"]

    latest_date = max(dates)
    if isinstance(date_filter, str) and date_filter.lower() == "all":
        filtered = list(zip(dates, prices))
    else:
        date_filter = latest_date - timedelta(days=date_filter)
        filtered = [(d, p) for d, p in zip(dates, prices) if d >= date_filter]

    dates, prices = zip(*filtered) if filtered else ([], [])

    color = '#05f746' if prices and prices[-1] >= prices[0] else '#f70505'
    # -------------------------------------------
    # 1. Create line plots for Close/Last
    # -------------------------------------------
    fig = go.Figure(
    data=[
        go.Scatter(
            x=dates,
            y=prices,
            mode='lines',
            name='Close Price',
            line=dict(color=color),
            hovertemplate='%{y:.2f}<extra></extra>'
        ),
    ],
    # -------------------------------------------
    # 1.5 Customize layout of the graph with hover over interaction, namings, and information
    # -------------------------------------------
    layout=go.Layout(
        title_text=f"Daily Closing Price for {source}",
        hovermode='x unified',
        xaxis=dict(
            title_text='Date',
            unifiedhovertitle=dict(
                text='<b>%{x|%A, %B %d, %Y}</b>'
            )
        ),
        yaxis=dict(
            title_text='Price (USD)',
            tickprefix='$'
        )
    )
)
    # -------------------------------------------
    # 2. Show the graph
    # -------------------------------------------
    return fig.to_html(full_html = False)


def plot_updown_trend(results):
    datesData = [i["Date"] for i in results[0]]
    pricesData = [i["Close/Last"] for i in results[0]]
    trendData = [i["Trend"] for i in results[0]]
    sample_days = results[1]
    
    fig = go.Figure(
        data=[
            go.Scatter(
                x=datesData,
                y=pricesData,
                mode='lines',
                name='Close Price'
            ),
        ],
        layout=go.Layout(
            title_text=f"Trend line for last {sample_days} samples",
            hovermode='x unified',
            xaxis=dict(
                title_text='Date',
                unifiedhovertitle=dict(
                    text='<b>%{x|%A, %B %d,%Y}</b>'
                )
            ),
            yaxis=dict(
                title_text='Price (USD)',
                tickprefix='$'
            )
        )
    )
    fig.add_trace(
        go.Scatter(
            x = datesData[-sample_days:],
            y = trendData[-sample_days:],
            name = 'Trend')
        )
    # fig.show()
    return fig.to_html(full_html = False)

def plot_max_profit(stockData, results):
    """
    https://plotly.com/python/candlestick-charts
    """
    datesData = stockData['Date']
    indexStart = datesData.index(results[0])
    indexEnd = datesData.index(results[1])
    datesData = datesData[indexStart:indexEnd]
    openData = stockData['Open'][indexStart:indexEnd]
    highData = stockData['High'][indexStart:indexEnd]
    lowData = stockData['Low'][indexStart:indexEnd]
    closeData = stockData['Close/Last'][indexStart:indexEnd]

    # indexBuy = datesData.index(results[3])
    # indexSell = datesData.index(results[4])

    fig = go.Figure(
        data=[go.Candlestick(x=datesData,
        open=openData,
        high=highData,
        low=lowData,
        close=closeData)],
        layout=go.Layout(
            title_text=f"Max Profit betwween {results[0]} and {results[1]} is $"+"{:.2f}".format(results[2]),
            hovermode='x unified',
            xaxis=dict(
                title_text='Date',
                unifiedhovertitle=dict(
                    text='<b>%{x|%A, %B %d,%Y}</b>'
                )
            ),
            yaxis=dict(
                title_text='Price (USD)',
                tickprefix='$'
            )
        )
    )
    print(results[3]['buy_date'])
    print(results[3]['buy_price'])
    print(type(results[3]['buy_date']))
    print(type(results[3]['buy_price']))
    fig.add_trace(go.Scatter(
        x=results[3]['buy_date'], 
        y=results[3]['buy_price'],
        mode = 'markers',
        marker = dict(color='green',
                      symbol = 'diamond',
                      size = 10),
                      name = 'Buy Day'
                      )
                    )
    fig.add_trace(go.Scatter(
        x=results[3]['sell_date'], 
        y=results[3]['sell_price'],
        mode = 'markers',
        marker = dict(color='red',
                      symbol = 'diamond',
                      size = 10),
                      name = 'Sell Day'
                      )
                    )
    # fig.show()
    return fig.to_html(full_html = False)

def plot_daily_ret(results, source):
    """
    results: list of dicts or tuples/namedtuples with 'Date' and 'Daily Return'
    Example dict: {'Date': datetime, 'Daily Return': 0.01}
    Example tuple: (datetime, 0.01) or namedtuple with fields 'Date' and 'Daily Return'
    """
    
    dates = []
    daily_returns = []
    # -------------------------------------------
    # Extract dates and daily returns from results
    # -------------------------------------------
    for i in results:
        # If i is a dict
        if isinstance(i, dict):
            date = i.get("Date")
            ret = i.get("Daily Return")
        else:
            continue  # skip malformed entries

        # Convert string date to datetime if needed
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                pass  # keep as string if format unknown

        dates.append(date) # Append the date to the list
        daily_returns.append(ret) # Append the daily return to the list

    # -------------------------------------------
    # Build figure
    # -------------------------------------------
    # line plot with markers and hover over interaction
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=daily_returns,
        mode="lines+markers",
        name="Daily Returns",
        line=dict(color="blue", width=2),
        hovertemplate='%{x}<br>Return: %{y:.2%}<extra></extra>'
    ))
    # -------------------------------------------
    # Customize layout of the graph with hover over interaction, namings, and information
    # -------------------------------------------
    fig.update_layout(
        title=f"{source} Daily Returns",
        xaxis_title="Date",
        yaxis_title="Daily Return",
        template="plotly_white",
        yaxis=dict(tickformat=".2%")
    )

    return fig.to_html(full_html=False) # Return the HTML representation of the figure