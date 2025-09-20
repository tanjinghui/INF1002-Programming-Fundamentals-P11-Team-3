from datetime import datetime


def ols_regression(x_data, y_data):
    """
    !!!this function was made by Google AI and editted + debugged by JacobLeow!!!
    
    Implements Ordinary Least Squares (OLS) regression without external libraries.

    Args:
        x_data (list): A list of independent variable values.
        y_data (list): A list of dependent variable values.

    Returns:
        tuple: A tuple containing the slope (m) and intercept (b) of the 
               regression line.
    """
    n = len(x_data)
    if len(x_data) != len(y_data):
        raise ValueError("len_x_data != len_y_data")
    
    # Calculate sums
    # print(x_data[:10])
    # print(y_data[:10])
    sum_x = sum(x_data)
    sum_y = sum(y_data)
    sum_xy = sum(x * y for x, y in zip(x_data, y_data))
    sum_x_squared = sum(x**2 for x in x_data)

    # Calculate slope
    numerator_slope = (n * sum_xy) - (sum_x * sum_y)
    denominator_slope = (n * sum_x_squared) - (sum_x**2)
    if denominator_slope == 0:
        raise ValueError("Denominator for slope is zero. Cannot perform OLS.")
    slope = numerator_slope / denominator_slope

    # Calculate intercept 
    intercept = (sum_y - slope * sum_x) / n
    # print(f"Slope: {slope}\nIntercept:{intercept}")

    return slope, intercept


def trend_finder(stockData: dict [str,list[object]], start_date: datetime, end_date: datetime, sample_days: int) -> tuple:
    """
    NOTE:
    assume stockData is sorted by date
    
    return values:
    (list) dates: list of dates 
    (list) prices: list of closing prices
    (int) indexStart: index of start_date in dates
    (int) indexEnd: index of end_date in dates
    (int) sample_days: number of days to sample for trend line
    (list) trend_data: prices for trend line for last sample_days
    (str) errorMsg: error message if any
    (bool) bullOrBear: True if bull trend, False if bear trend, None if flat trend

    reference:
    https://www.geeksforgeeks.org/python/python-program-to-get-total-business-days-between-two-dates
    https://stackoverflow.com/questions/65012886/plotly-how-to-calculate-and-illustrate-the-upper-and-lower-50-of-a-trend-line
    """
    
    dates = [i for i in stockData["Date"]]
    prices = [i for i in stockData["Close/Last"]]
    index = [i for i,v in enumerate(stockData["Date"])]
    errorMsg = None
    bullOrBear = None
    result = []
    if (end_date-start_date).days <= 0:
        errorMsg = "Swapped start and end date"
        start_date,end_date = end_date,start_date
    startDate = binary_search(dates, start_date)
    endDate = binary_search(dates, end_date)
    num_weedays_selected = endDate - startDate + 1
    if  sample_days > num_weedays_selected:
        sample_days = num_weedays_selected//2
        errorMsg = "Trend window set to default ratio of date range"
    dates = dates[startDate : endDate + 1]
    prices = prices[startDate : endDate + 1]
    index = index[startDate : endDate + 1]
    try:
        trend,const = ols_regression(
            index[-sample_days:],
            prices[-sample_days:]
            )
    except ValueError as e:
        trend_data = [None for i in index]
        errorMsg = str(e)
        for date, price, trend in zip(dates, prices, trend_data):
            result.append({"Date" : date, "Close/Last" : price, "Trend" : trend})
        return (result, sample_days, errorMsg, bullOrBear)
    if trend > 0.15:
        bullOrBear = True
    elif trend < -0.15:
        bullOrBear = False
    else:
        pass
    trend_data = [const + (trend*i) for i in index]
    for date, price, trend in zip(dates, prices, trend_data):
        result.append({"Date" : date, "Close/Last" : price, "Trend" : trend})
    return (result, sample_days, errorMsg, bullOrBear)


# Define a function to calculate the maximum profit from buying and selling stocks
def max_profit(stockData, start_date, end_date):
    """
    NOTE:
    assume stockData is sorted by date
    assume you can only buy once and sell once
    assume all stocks are used in one transaction

    (list) stock_price: list of stock prices)

    return values:
    (datetiume) start_date: start date for calculation
    (datetiume) end_date: end date for calculation
    (int) max_profit_amt: maximum profit amount
    (datetime) buyDay: which day the stock was bought
    (datetime) sellDay: which day the stock was sold
    (str) errorMsg: error message if any
    """
    # Initialize the maximum profit amount to zero
    max_profit_amt = 0
    dates = [i for i in stockData["Date"]]
    priceHigh = [i for i in stockData["High"]]
    priceClose = [i for i in stockData["Close/Last"]]
    errorMsg = None
    if (end_date-start_date).days <= 0:
        errorMsg = "Swapped start and end date"
        start_date,end_date = end_date,start_date
    startDate = binary_search(dates, start_date)
    endDate = binary_search(dates, end_date)

    if len(dates) < 2:
        return {
            'total_profit': 0,
            'transactions': [],
            'date_range': [start_date, end_date],
            'error': 'Need at least 2 days for consecutive day trading'
        }
    
    transaction = {
            'buy_date': [],
            'sell_date': [],
            'buy_price': [],
            'sell_price': [],
            'profit':[],
            'is_profitable': []
        }
    max_profit_amt = 0
    dates = dates[startDate:endDate+1]
    priceHigh = priceHigh[startDate:endDate+1]
    priceClose = priceClose[startDate:endDate+1]

    for i in range(len(dates) - 1):
        buy_price = priceClose[i]    # Buy at close of current day
        sell_price = priceHigh[i + 1]  # Sell at high of next day
        profit = sell_price - buy_price
        transaction['buy_date'].append(dates[i])
        transaction['sell_date'].append(dates[i+1])
        transaction['buy_price'].append(buy_price)
        transaction['sell_price'].append(sell_price)
        transaction['profit'].append(profit)
        transaction['is_profitable'].append(profit > 0)

    indices = [index for index, value in enumerate(transaction['is_profitable']) if value == False]

    for i in indices[::-1]:
        transaction['buy_date'].pop(i)
        transaction['sell_date'].pop(i)
        transaction['buy_price'].pop(i)
        transaction['sell_price'].pop(i)
        transaction['profit'].pop(i)
        transaction['is_profitable'].pop(i)

    max_profit_amt = sum(transaction["profit"])

    # Return the maximum profit amount
    return [start_date, end_date, max_profit_amt, transaction, errorMsg]


def binary_search(dates: list[datetime], target: datetime) -> int:
    # -------------------------------------------
    # 1. Standard binary search with two pointers that finds the date by dividing by 2 each search
    # -------------------------------------------
    start = 0
    end = len(dates) - 1

    while start <= end:
        mid = (start + end) // 2
        if dates[mid] >= target:
            end = mid - 1
        else:
            start = mid + 1
        
    return start


def calc_sma(close_prices: list[float], days_window: int) -> list[float]:
    # -------------------------------------------
    # 1. Populate sma_prices list so that dates with less than window days will have None value
    # 2. Returns None value list as the window is too big for the selected range
    # ------------------------------------------- 
    sma_prices = [None] * len(close_prices)
    if len(close_prices) < days_window:
        return sma_prices
    
    # ------------------------------------------- 
    # 3. Calculate sum of first window and update it into sma_prices
    # ------------------------------------------- 
    closeSum = sum(close_prices[:days_window])
    sma_prices[days_window - 1] = round(closeSum / days_window, 2)

    # ------------------------------------------- 
    # 4. For loop over each price/date and adding the current while subtracting the earliest price/date
    # 5. Calculate SMA by diving by window and rounding off to 2 d.p. while updating sma_prices
    # ------------------------------------------- 
    for i in range(days_window, len(close_prices)):
        closeSum += close_prices[i] - close_prices[i - days_window]
        sma_prices[i] = round(closeSum / days_window, 2)
    
    return sma_prices


def calc_ema(close_prices: list[float], smaData: list[float], days_window: int) -> list[float]:
    # -------------------------------------------
    # 1. Builds on from calc_sma, where results from SMA is multiplied by the multiplier to give EMA
    # -------------------------------------------
    multiplier = 2 / (days_window + 1)
    n = len(smaData)
    ema_prices = [None] * n

    ema_prices[days_window - 1] = smaData[days_window - 1]

    for i in range(days_window, n):
        ema_prices[i] = round((close_prices[i] * multiplier) + (ema_prices[i - 1] * (1 - multiplier)), 2)
    
    return ema_prices


def moving_average(stockData: dict[str, list[object]], start_date: datetime, end_date: datetime, days_window: int) -> list[dict[str, object]]:
    # -------------------------------------------
    # 1. Get the starting and end dates that the user wants
    # 2. Calls for binary search for both dates to return their indexes in dates
    # 3. Filters both dates and prices so calc_sma will be more efficient as there is less data
    # -------------------------------------------
    dates = stockData["Date"]
    close_prices = stockData["Close/Last"]

    startDate = binary_search(dates, start_date)
    endDate = binary_search(dates, end_date)

    filtered_dates = dates[startDate : endDate + 1]
    filtered_prices = close_prices[startDate : endDate + 1]

    # -------------------------------------------
    # 4. Calculate SMA and EMA
    # -------------------------------------------
    smaResults = calc_sma(filtered_prices, days_window)
    emaResults = calc_ema(filtered_prices, smaResults, days_window)

    # -------------------------------------------
    # 5. Append smaResults and emaResults into maData and return results
    # -------------------------------------------
    maData = []
    for date, price, sma, ema in zip(filtered_dates, filtered_prices, smaResults, emaResults):
        maData.append({"Date" : date, "Close/Last" : price, "SMA" : sma, "EMA" : ema})
    return maData


def daily_ret(stockData):
    dates = stockData["Date"]
    closes = stockData["Close/Last"]
    # Calculate daily returns
    daily_returns = [None]  # no return for first day
    for i in range(1, len(closes)):
        ret = (closes[i] - closes[i-1]) / closes[i-1]
        daily_returns.append(ret)

    # Return as list of dicts (date, daily return)
    return [{"Date": d, "Daily Return": r} for d, r in zip(dates, daily_returns)]