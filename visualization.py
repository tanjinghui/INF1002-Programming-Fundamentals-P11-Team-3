import plotly.graph_objects as go

def plot_smaGraph(smaData, days_window):
#   smaData: type dict
#   days_window: type int
    dates = [i for i in smaData['Date']]
    prices = [i for i in smaData["Close/Last"]]
    sma = [i for i in smaData["SMA"]]

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
                name=f"[days_window]-day SMA"
            )
        ],
        layout=go.layout(
            title_text="Daily Closing Price vs Simple Moving Average",
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