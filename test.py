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
def maxProfit(prices: list[int]) -> int:
    #initializes profit to 0 at start
    profit = 0
    #for loops through the list of prices
    for i in range(1, len(prices)):
        # gets the ith index and subtracts the value from the previous index
        cur = prices[i] - prices[i-1]
        # if the value subtracted is above 0 then cumulate the profit into profit
        if cur > 0:
            profit += cur
    #return profit
    return profit

print(maxProfit([7,1,5,3,6,4]))
print(maxProfit([1,2,3,4,5]))
print(maxProfit([7,6,4,3,1]))