from flask import Flask, render_template, request
from datetime import datetime
import csv
import functions
import visualization

app = Flask(__name__)

def loadData(csvfile):
    # -------------------------------------------
    # 1. Initialize empty list to append data later
    # -------------------------------------------
    dates = []
    close_prices = []
    volume = []
    open_price = []
    high_price = []
    low_price = []

    # -------------------------------------------
    # 2. Reads data from csv file, cleans the data and appends into list
    # -------------------------------------------
    with open(csvfile, "r") as csvfile:
        read = csv.DictReader(csvfile)
        for i in read:
            date_data = datetime.strptime(i["Date"], "%m/%d/%Y")
            close_data = float(i["Close/Last"].replace("$", "").strip())
            volume_data = int(i["Volume"])
            open_data = float(i["Open"].replace("$", "").strip())
            high_data = float(i["High"].replace("$", "").strip())
            low_data = float(i["Low"].replace("$", "").strip())
            dates.append(date_data)
            close_prices.append(close_data)
            volume.append(volume_data)
            open_price.append(open_data)
            high_price.append(high_data)
            low_price.append(low_data) 

    # -------------------------------------------
    # 3. Combine the data together by index in order to sort all data together by date
    # 4. Unpacks the data into their respective lists
    # -------------------------------------------
    combineSort = sorted(zip(dates, close_prices, volume, open_price, high_price, low_price), key = lambda dates: dates[0])
    dates, close_prices, volume, open_price, high_price, low_price = zip(*combineSort)

    return {"Date" : list(dates), "Close/Last" : list(close_prices), "Volume" : list(volume), "Open" : list(open_price), "High" : list(high_price), "Low" : list(low_price)}

stockData = loadData("data/apple.csv")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sma", methods = ["GET", "POST"])
def smaPage():
    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        days_window = int(request.form.get("days_window"))

    return render_template("sma.html")

if __name__ == "__main__":
    app.run(debug=True)



#references
#https://www.w3schools.com/python/default.asp
#https://en.wikipedia.org/wiki/Moving_average
#https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp
#https://docs.python.org/3/library/csv.html
#https://www.geeksforgeeks.org/python/flask-http-methods-handle-get-post-requests/
#https://plotly.com/python/line-and-scatter/#linear-regression-and-other-trendlines