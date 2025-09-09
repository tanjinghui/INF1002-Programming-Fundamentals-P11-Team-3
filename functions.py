from datetime import datetime,timedelta

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

def trend_finder(stockData, start_date, end_date, sample_days):
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
    """
    
    dates = [i for i in stockData["Date"]]
    prices = [i for i in stockData["Close/Last"]]
    index = [i for i,v in enumerate(stockData["Date"])]
    errorMsg = None
    if (end_date-start_date).days <= 0:
        errorMsg = "Swapped start and end date"
        start_date,end_date = end_date,start_date
    while start_date not in stockData['Date']:
        errorMsg = "Selected closest weekday for start date"
        start_date -= timedelta(days=1)
    while end_date not in stockData['Date']:
        errorMsg = "Selected closest weekday for end date"
        end_date -= timedelta(days=1)
        print(f"end_date: {end_date}")
    print(f"erroMsg: {errorMsg}, start_date: {start_date}, end_date: {end_date}")
    dates_to_validate_trend_line_len = (start_date + timedelta(idx + 1) for idx in range((end_date - start_date).days))
    result_to_validate_trend_line_len = sum(1 for day in dates_to_validate_trend_line_len if day.weekday() < 5)
    if  sample_days > result_to_validate_trend_line_len:
        sample_days = result_to_validate_trend_line_len//2
        errorMsg = "Trend window set to default ratio of date range"
    indexStart = dates.index(start_date)
    indexEnd = dates.index(end_date)
    trend,const = ols_regression(
        index[indexEnd-sample_days : indexEnd],
        prices[indexEnd-sample_days : indexEnd]
        )
    # print(trend)
    if trend > 0.35:
        bullOrBear = True
    elif trend < -0.35:
        bullOrBear = False
    else:
        bullOrBear = None
    trend_data = [const + (trend*i) for i in index[indexEnd-sample_days:indexEnd]]
    return([dates, prices, indexStart, indexEnd, sample_days, trend_data, errorMsg, bullOrBear])

# Define a function to calculate the maximum profit from buying and selling stocks
def max_profit(stockData, start_date, end_date):
    """
    NOTE:
    assume stockData is sorted by date
    assume you can only buy once and sell once
    assume all stocks are used in one transaction

    (list) stock_price: list of stock prices)

    return values:
    (int) max_profit_amt: maximum profit amount
    """
    # Initialize the maximum profit amount to zero
    max_profit_amt = 0
    dates = [i for i in stockData["Date"]]
    priceLow = [i for i in stockData["Low"]]
    priceHigh = [i for i in stockData["High"]]
    errorMsg = None
    if (end_date-start_date).days <= 0:
        errorMsg = "Swapped start and end date"
        start_date,end_date = end_date,start_date
    while start_date not in stockData['Date']:
        errorMsg = "Selected closest weekday for start date"
        start_date -= timedelta(days=1)
    while end_date not in stockData['Date']:
        errorMsg = "Selected closest weekday for end date"
        end_date -= timedelta(days=1)
        print(f"end_date: {end_date}")
    print(f"erroMsg: {errorMsg}, start_date: {start_date}, end_date: {end_date}")
    indexStart = dates.index(start_date)
    indexEnd = dates.index(end_date)
    priceLow, priceHigh = priceLow[indexStart : indexEnd], priceHigh[indexStart : indexEnd]
    buyDay,sellDay = None, None

    # Iterate through the stock prices using a nested loop
    for i in range(len(priceLow)):
        # Initialize the profit amount for the current day to zero
        profit_amt = 0

        # Iterate through the subsequent days to find potential profit
        for j in range(i+1, len(priceHigh)):
            # Calculate the profit by subtracting the buying price from the selling price
            profit_amt = priceHigh[j] - priceLow[i]

            # Update the maximum profit if the current profit is greater, save which dates the stock was bought and sold on.
            if profit_amt > max_profit_amt:
                max_profit_amt = profit_amt
                buyDay, sellDay = dates[i], dates[j]

    # Return the maximum profit amount
    return [max_profit_amt, buyDay, sellDay, errorMsg]

def binary_search(dates, target):
    pass


def calc_sma(close_prices, window):
    pass

def simple_moving_average(stockData, start_date, end_date, days_window):
    pass

def weighted_moving_average(stockData):
    pass


def exponential_moving_average(stockData):
    pass