import plotly.graph_objects as go
from datetime import datetime

def plot_smaGraph(smaData, days_window):
    dates = [i["Date"] for i in smaData]
    prices = [i["Close/Last"] for i in smaData]
    sma = [i["SMA"] for i in smaData]
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
        )
    ],
    # -------------------------------------------
    # 1.5 Customize layout of the graph with hover over interaction, namings, and information
    # -------------------------------------------
    layout=go.Layout(
        title_text="Daily Closing Price vs Simple Moving Average",
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
    datesData = results[0]
    pricesData = results[1]
    indexStart = results[2]
    indexEnd = results[3]
    sample_days = results[4]
    trendData = results[5]
    fig = go.Figure(
        data=[
            go.Scatter(
                x=datesData[indexStart:indexEnd],
                y=pricesData[indexStart:indexEnd],
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
            x = datesData[indexEnd-sample_days:indexEnd],
            y = trendData[:],
            name = 'trend')
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

    indexBuy = datesData.index(results[3])
    indexSell = datesData.index(results[4])

    fig = go.Figure(
        data=[go.Candlestick(x=datesData,
        open=openData,
        high=highData,
        low=lowData,
        close=closeData)],
        layout=go.Layout(
            title_text=f"Max Profit betwween {results[0]} and {results[1]} is ${results[2]}",
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
    fig.add_trace(go.Scatter(
        x=[datesData[indexBuy]], 
        y=[highData[indexBuy]],
        mode = 'markers',
        marker = dict(color='green',
                      symbol = 'diamond',
                      size = 10),
                      name = 'Buy Day'
                      )
                    )
    fig.add_trace(go.Scatter(
        x=[datesData[indexSell]], 
        y=[highData[indexSell]],
        mode = 'markers',
        marker = dict(color='red',
                      symbol = 'diamond',
                      size = 10),
                      name = 'Buy Day'
                      )
                    )
    # fig.show()
    return fig.to_html(full_html = False)

def plot_daily_ret(results):
    """
    results: list of dicts or tuples/namedtuples with 'Date' and 'Daily Return'
    Example dict: {'Date': datetime, 'Daily Return': 0.01}
    Example tuple: (datetime, 0.01) or namedtuple with fields 'Date' and 'Daily Return'
    """
    
    dates = []
    daily_returns = []

    for i in results:
        # If i is a dict
        if isinstance(i, dict):
            date = i.get("Date")
            ret = i.get("Daily Return")
        # If i is a namedtuple
        elif hasattr(i, "_fields"):
            date = getattr(i, "Date", None)
            ret = getattr(i, "Daily Return", None)
        # If i is a plain tuple
        else:
            if len(i) >= 2:
                date, ret = i[0], i[1]
            else:
                continue  # skip malformed entries

        # Convert string date to datetime if needed
        if isinstance(date, str):
            try:
                date = datetime.fromisoformat(date)
            except ValueError:
                pass  # keep as string if format unknown

        dates.append(date)
        daily_returns.append(ret)

    # Build figure
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=daily_returns,
        mode="lines+markers",
        name="Daily Returns",
        line=dict(color="blue", width=2),
        hovertemplate='%{x}<br>Return: %{y:.2%}<extra></extra>'
    ))

    fig.update_layout(
        title="Apple Daily Returns",
        xaxis_title="Date",
        yaxis_title="Daily Return",
        template="plotly_white"
    )

    return fig.to_html(full_html=False)