from datetime import datetime


def ols_regression(x_data, y_data) -> tuple:
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

    return (slope, intercept)


def trend_finder(stockData: dict [str,list[object]], start_date: datetime, end_date: datetime, sample_days: int) -> tuple:
    """
    NOTE:
    assume stockData is sorted by date
    
    return values:
    (dict) results: a dict with keys: "Date", "Close/Last", "Trend"
        (key) Date: list of dates; Datetime obj 
        (key) Close/Last: list of closing prices; float
        (key) Trend: prices for trend line for last sample_days
    (int) sample_days: number of days to sample for trend line
    (str) errorMsg: error message if any
    (bool) bullOrBear: True if bull trend, False if bear trend, None if flat trend

    reference:
    https://www.geeksforgeeks.org/python/python-program-to-get-total-business-days-between-two-dates
    https://stackoverflow.com/questions/65012886/plotly-how-to-calculate-and-illustrate-the-upper-and-lower-50-of-a-trend-line
    """
    # -------------------------------------------
    # Retrieve and init data and variables
    # -------------------------------------------
    dates = [date for date in stockData["Date"]]
    prices = [close for close in stockData["Close/Last"]]
    index = [index for index in range(len(stockData["Date"]))]
    errorMsg = None
    bullOrBear = None
    result = []
    # -------------------------------------------
    # start and end date input validation
    # -------------------------------------------
    if (end_date-start_date).days <= 0:
        errorMsg = "Swapped start and end date"
        start_date,end_date = end_date,start_date
    # -------------------------------------------
    # Search for valid date in data set (weekend dates do not have data)
    # -------------------------------------------
    startDate = binary_search(dates, start_date)
    endDate = binary_search(dates, end_date)
    num_weedays_selected = endDate - startDate + 1
    # -------------------------------------------
    # sample days input validation
    # -------------------------------------------
    if  sample_days > num_weedays_selected:
        sample_days = num_weedays_selected//2
        errorMsg = "Trend window set to default ratio of date range"
    # -------------------------------------------
    # Trim down local copy of data set
    # -------------------------------------------
    dates = dates[startDate : endDate + 1]
    prices = prices[startDate : endDate + 1]
    index = index[startDate : endDate + 1]
    # -------------------------------------------
    # Attempt to generate trend data
    # -------------------------------------------
    try:
        trend,const = ols_regression(
            index[-sample_days:],
            prices[-sample_days:]
            )
    except ValueError as e:
        # -------------------------------------------
        # return some value in case of error so code will still present something
        # -------------------------------------------
        trend_data = [None for i in index]
        errorMsg = str(e)
        for date, price, trend in zip(dates, prices, trend_data):
            result.append({"Date" : date, "Close/Last" : price, "Trend" : trend})
        return (result, sample_days, errorMsg, bullOrBear)
    # -------------------------------------------
    # prepare bullish or bearish trend indicator, 0.15 was arbitrary, decided by Programmer
    # -------------------------------------------
    if trend > 0.15:
        bullOrBear = True
    elif trend < -0.15:
        bullOrBear = False
    else:
        bullOrBear = None
    # -------------------------------------------
    # compute actual price for trend line graph points 
    # -------------------------------------------
    trend_data = [const + (trend*i) for i in index]
    # -------------------------------------------
    # Prepare data for return
    # -------------------------------------------
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
        # Exact match found
        if dates[mid] == target: 
            return mid
        # Move left if mid date is after or equal to target
        elif dates[mid] > target: 
            end = mid - 1
        # Move right if mid date is before target
        else: 
            start = mid + 1
    # -------------------------------------------
    # 2. If date not found, return the closest date that is after the target
    # -------------------------------------------
    return start


def calc_sma(close_prices: list[float], days_window: int) -> list[float]:
    # -------------------------------------------
    # 1. Populate sma_prices list so that dates with less than window days will have None value
    # ------------------------------------------- 
    n = len(close_prices)
    sma_prices = [None] * n
    
    # ------------------------------------------- 
    # 2. Calculate sum of first window and update it into sma_prices
    # ------------------------------------------- 
    closeSum = sum(close_prices[:days_window])
    sma_prices[days_window - 1] = round(closeSum / days_window, 2)

    # ------------------------------------------- 
    # 3. For loop over each price/date and adding the current while subtracting the earliest price/date
    # 4. Calculate SMA by diving by window and rounding off to 2 d.p. while updating sma_prices
    # ------------------------------------------- 
    for i in range(days_window, n):
        closeSum += close_prices[i] - close_prices[i - days_window]
        sma_prices[i] = round(closeSum / days_window, 2)
    
    return sma_prices


def calc_ema(close_prices: list[float], smaData: list[float], days_window: int) -> list[float]:
    # -------------------------------------------
    # 1. Builds on from calc_sma, where results from SMA is multiplied by the multiplier to give EMA
    # -------------------------------------------
    multiplier = 2 / (days_window + 1)
    # -------------------------------------------
    # 2. Creates ema_prices list so that dates with less than window days will have None value
    # -------------------------------------------
    n = len(smaData)
    ema_prices = [None] * n

    ema_prices[days_window - 1] = smaData[days_window - 1]
    # -------------------------------------------
    # 3. For loop over each price/date and calculating EMA using the formula, rounding off to 2 d.p. while updating ema_prices
    # -------------------------------------------
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

    # Edge case handling, return empty list if no data or invalid input
    if not dates or not close_prices or days_window <= 0:
        return []
    if start_date > end_date:
        return []

    startDate = binary_search(dates, start_date)
    endDate = binary_search(dates, end_date)

    # Edge case handling, return empty list if no data in range
    if startDate >= len(dates) or endDate < 1:
        return []

    filtered_dates = dates[startDate : endDate + 1]
    filtered_prices = close_prices[startDate : endDate + 1]

    # Edge case handling, return empty list if not enough data for the window
    if len(filtered_prices) < days_window:
        return []
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
        maData.append({"Date" : date, "Close/Last" : round(price, 2), "SMA" : sma, "EMA" : ema})
    return maData


class SegmentTree:
    # -------------------------------------------
    # 1. Segment Tree data structure to allow range queries for average and max in O(log n) time
    # -------------------------------------------
    def __init__(self, stockData: list[float]) -> None:
        self.n = len(stockData)
        # Initialize max and sum segment tree with size 4*n to accommodate all nodes
        self.sum_tree = [0] * (4 * self.n)
        self.max_tree = [0] * (4 * self.n)
        # Build both segment trees
        self.build_sum_tree(stockData, 0, 0, self.n - 1)
        self.build_max_tree(stockData, 0, 0, self.n - 1)

    # -------------------------------------------
    # 2. Build the segment tree recursively, where each node represents the sum of a segment
    # -------------------------------------------
    def build_sum_tree(self, stockData: list[float], node: int, left: int, right: int) -> None:
        # Node that represents a single date
        if left == right: 
            self.sum_tree[node] = stockData[left]
        # Internal node that represents the sum of its children
        else: 
            mid = (left + right) // 2
            self.build_sum_tree(stockData, 2 * node + 1, left, mid)
            self.build_sum_tree(stockData, 2 * node + 2, mid + 1, right)
            self.sum_tree[node] = self.sum_tree[2 * node + 1] + self.sum_tree[2 * node + 2]

    # -------------------------------------------
    # 3. Calculate range sum and average using the segment tree
    # -------------------------------------------
    def range_sum(self, node: int, left: int, right: int, query_left: int, query_right: int) -> int:
        # If query range is outside the node range, return 0
        if query_right < left or query_left > right:
            return 0
        # If node range is completely within query range, return the node's sum
        if query_left <= left and right <= query_right: 
            return self.sum_tree[node]
        # Query range is partially inside, so split the query into left and right children, returning the sum of both
        mid = (left + right) // 2 
        left_sum = self.range_sum(2 * node + 1, left, mid, query_left, query_right)
        right_sum = self.range_sum(2 * node + 2, mid + 1, right, query_left, query_right)
        return left_sum + right_sum

    def range_average(self, start_date: int, end_date: int) -> float:
        # Validate date range
        if start_date < 0 or end_date >= self.n or start_date > end_date:
            raise ValueError("Invalid date range")
        # Calculate total sum in the range and divide by number of days to get average
        total_sum = self.range_sum(0, 0, self.n - 1, start_date, end_date)
        return total_sum / (end_date - start_date + 1)
    
    # -------------------------------------------
    # 4. Build another segment tree for range max queries
    # -------------------------------------------
    def build_max_tree(self, stockData: list[float], node: int, left: int, right: int) -> None:
        # Node that represents a single date
        if left == right: 
            self.max_tree[node] = stockData[left]
        # Internal node that represents the max of its children
        else: 
            mid = (left + right) // 2
            self.build_max_tree(stockData, 2 * node + 1, left, mid)
            self.build_max_tree(stockData, 2 * node + 2, mid + 1, right)
            self.max_tree[node] = max(self.max_tree[2 * node + 1], self.max_tree[2 * node + 2])

    def call_range_max(self, node: int, left: int, right: int, query_left: int, query_right: int) -> float:
        # If query range is outside the node range, return negative infinity, negative infinity is used so negative values are considered
        if query_right < left or query_left > right:
            return float('-inf')
        # If node range is completely within query range, return the node's max
        if query_left <= left and right <= query_right:
            return self.max_tree[node]
        # Query range is partially inside, so split the query into left and right children, returning the max of both
        mid = (left + right) // 2
        left_max = self.call_range_max(2 * node + 1, left, mid, query_left, query_right)
        right_max = self.call_range_max(2 * node + 2, mid + 1, right, query_left, query_right)
        return max(left_max, right_max)

    def range_max(self, start_date: int, end_date: int) -> float:
        # Validate date range
        if start_date < 0 or end_date >= self.n or start_date > end_date:
            raise ValueError("Invalid date range")
        # Calculate the maximum in the range
        return self.call_range_max(0, 0, self.n - 1, start_date, end_date)
    

def daily_ret(stockData):
    dates = stockData["Date"]
    closes = stockData["Close/Last"]
    # -------------------------------------------
    # Calculate daily returns
    # -------------------------------------------
    daily_returns = [None]  # no return for non-trading day
    # -------------------------------------------
    # Calculate daily returns using the formula: (current_close - previous_close) / previous_close
    # -------------------------------------------
    for i in range(1, len(closes)):
        ret = (closes[i] - closes[i-1]) / closes[i-1]
        daily_returns.append(ret) # Append the calculated return to the list
    # -------------------------------------------
    # Return as list of dicts (date, daily return)
    # -------------------------------------------
    return [{"Date": d, "Daily Return": r} for d, r in zip(dates, daily_returns)]