import plotly.graph_objects as go

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
