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
    # NOTE:
    # assume stockData is sorted by date
    # assume start_date < end_date
    # assume sample_days < len(end_date - start_date)
    # assume indexEnd-sample_days > 0
    #
    # return values:
    # (list) dates: list of dates 
    # (list) prices: list of closing prices
    # (int) indexStart: index of start_date in dates
    # (int) indexEnd: index of end_date in dates
    # (list) trend_data: prices for trend line for last sample_days
    # (bool) bullOrBear: True if bull trend, False if bear trend, None if flat trend
    #
    dates = [i for i in stockData["Date"]]
    prices = [i for i in stockData["Close/Last"]]
    index = [i for i,v in enumerate(stockData["Date"])]
    indexStart = dates.index(start_date)
    indexEnd = dates.index(end_date)
    trend,const = ols_regression(
        index[indexEnd-sample_days : indexEnd],
        prices[indexEnd-sample_days : indexEnd]
        )
    print(trend)
    if trend > 0.35:
        bullOrBear = True
    elif trend < -0.35:
        bullOrBear = False
    else:
        bullOrBear = None
    trend_data = [const + (trend*i) for i in index[indexEnd-sample_days:indexEnd]]
    return([dates, prices, indexStart, indexEnd, trend_data, bullOrBear])

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