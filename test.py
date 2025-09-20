# # Define a function to calculate the maximum profit from buying and selling stocks
# def max_profit(stock_price):
#     # Initialize the maximum profit amount to zero
#     max_profit_amt = 0

#     # Iterate through the stock prices using a nested loop
#     for i in range(len(stock_price)):
#         # Initialize the profit amount for the current day to zero
#         profit_amt = 0

#         # Iterate through the subsequent days to find potential profit
#         for j in range(i+1, len(stock_price)):
#             # Calculate the profit by subtracting the buying price from the selling price
#             profit_amt = stock_price[j] - stock_price[i]

#             # Update the maximum profit if the current profit is greater
#             if profit_amt > max_profit_amt:
#                 max_profit_amt = profit_amt

#     # Return the maximum profit amount
#     return max_profit_amt


# # Test the function with a list of stock prices and print the result
# print(max_profit([224, 236, 247, 258, 259, 225]))

#ideal solution for Leetcode Question 122. 
# def maxProfit(prices: list[int]) -> int:
#     #initializes profit to 0 at start
#     profit = 0
#     #for loops through the list of prices
#     for i in range(1, len(prices)):
#         # gets the ith index and subtracts the value from the previous index
#         cur = prices[i] - prices[i-1]
#         # if the value subtracted is above 0 then cumulate the profit into profit
#         if cur > 0:
#             profit += cur
#     #return profit
#     return profit

# print(maxProfit([7,1,5,3,6,4]))
# print(maxProfit([1,2,3,4,5]))
# print(maxProfit([7,6,4,3,1]))


# ===========================================================yfinance sample code===================================================

import yfinance as yf
import pandas as pd


# Create a Ticker object for AAPL
apple = yf.Ticker("AAPL")

# Get historical market data for the last year
hist = apple.history(period="1y")

#              Open        High         Low       Close    Volume  Dividends  Stock Splits
# Date                                                                                 
# 2024-09-19  222.000000  223.100006  221.059998  222.429993  45892500        0.0           0.0
# 2024-09-20  223.000000  223.770004  221.750000  222.119995  44081000        0.0           0.0

# Download historical data for a list of tickers
strOfTickers = "AAPL MSFT GOOG"
data = yf.download(strOfTickers, start="2024-01-01", end="2024-09-20")
dates = [v.to_pydatetime() for v in data.index]
print(dates)

#data.keys()
# MultiIndex([( 'Close', 'AAPL'),
#             ( 'Close', 'GOOG'),
#             ( 'Close', 'MSFT'),
#             (  'High', 'AAPL'),
#             (  'High', 'GOOG'),
#             (  'High', 'MSFT'),
#             (   'Low', 'AAPL'),
#             (   'Low', 'GOOG'),
#             (   'Low', 'MSFT'),
#             (  'Open', 'AAPL'),
#             (  'Open', 'GOOG'),
#             (  'Open', 'MSFT'),
#             ('Volume', 'AAPL'),
#             ('Volume', 'GOOG'),
#             ('Volume', 'MSFT')],
#            names=['Price', 'Ticker'])
# names price means name of 1st column of keys i.e. Close, High, Low, Open, Volume
# names ticker means name of 2nd column of keys i.e. AAPL, GOOG, MSFT

# When doing multi download, must access type first, not ticker first
# i.e. ["Close"]["AAPL"] ["High"]["GOOG"]

# data_1 = data["Close"]["AAPL"]

for i in strOfTickers.split():
    dates = [v.to_pydatetime() for v in data.index]
    close_prices = [float(data["Close"][i][v]) for v in data["Close"][i].index]   #float(i["Close/Last"].replace("$", "").strip())
    volume = [int(data["Volume"][i][v]) for v in data["Volume"][i].index]  #int(i["Volume"])
    open_price = [float(data["Open"][i][v]) for v in data["Open"][i].index]      #float(i["Open"].replace("$", "").strip())
    high_price = [float(data["High"][i][v]) for v in data["High"][i].index]      #float(i["High"].replace("$", "").strip())
    low_price = [float(data["Low"][i][v]) for v in data["Low"][i].index]     #float(i["Low"].replace("$", "").strip())
combineSort = sorted(zip(dates, close_prices, volume, open_price, high_price, low_price), key = lambda dates: dates[0])
dates, close_prices, volume, open_price, high_price, low_price = zip(*combineSort)

# Access data for each ticker, for example, the closing prices
# print(data['Close'].head())

# info = apple.info

# Print specific details
# print("Sector:", info.get("sector"))
# print("Industry:", info.get("industry"))
# print("Website:", info.get("website"))
# print("Market Cap:", info.get("marketCap"))

# Get income statement
# income_stmt = apple.financials
# print("\nIncome Statement:")
# print(income_stmt)

# Get balance sheet
# balance_sheet = apple.balance_sheet
# print("\nBalance Sheet:")
# print(balance_sheet)

# Get all dividend payments
# dividends = apple.dividends
# print("\nDividends:")
# print(dividends)

# Get all stock splits
# splits = apple.splits
# print("\nSplits:")
# print(splits)




