from flask import Flask, render_template, request
from datetime import datetime,timedelta
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
    results = None
    start_date = None
    end_date = None
    days_window = None
    smaGraph = None

    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        days_window = int(request.form.get("days_window"))
        results = functions.simple_moving_average(stockData, start_date, end_date, days_window)
        smaGraph = visualization.plot_smaGraph(results, days_window)

    return render_template("sma.html", results = results, dayswindow = days_window, start_date = start_date, end_date = end_date, smaGraph= smaGraph)


@app.route("/trend", methods = ["GET", "POST"])
def trendPage():
    results = None
    start_date = None
    end_date = None
    trend_window = None
    trendGraph = None
    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        trend_window = int(request.form.get("trend_window"))
        results = functions.trend_finder(stockData, start_date, end_date, trend_window)
        trendGraph = visualization.plot_updown_trend(results)
        return render_template("trend.html", results = results, trendwindow = trend_window, stert_date = start_date, end_date = end_date, trendGraph= trendGraph, errorMsg=results[6], bullOrBear = results[7])
    return render_template("trend.html", results = None, trendwindow = None, stert_date = start_date, end_date = end_date, trendGraph= None, errorMsg=None, bullOrBear = None)


@app.route("/max_profit", methods = ["GET", "POST"])
def max_profit_Page():
    results = None
    start_date = None
    end_date = None
    maxProfitGraph = None
    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
#        trend_window = int(request.form.get("trend_window"))
        results = functions.max_profit(stockData, start_date, end_date)
        max_profit_Graph = visualization.plot_max_profit(stockData,results)
        return render_template("max_profit.html", results = results, stert_date = start_date, end_date = end_date, max_profit_Graph= max_profit_Graph, errorMsg=results[5])
    return render_template("max_profit.html", results = None, stert_date = start_date, end_date = end_date, max_profit_Graph= None, errorMsg=None)

@app.route("/daily_return", methods = ["GET", "POST"])
def daily_return_Page():
    results = None
    start_date = None
    end_date = None
    daily_ret_graph = None

    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        results = functions.daily_ret(stockData)
        # Filter results by date range
        if results and start_date and end_date:
            # Ensure date in result is datetime, convert if needed
            filtered = []
            for row in results:
                date_val = row["Date"]
                if isinstance(date_val, str):
                    try:
                        date_val = datetime.fromisoformat(date_val)
                    except Exception:
                        continue
                if start_date <= date_val <= end_date:
                    filtered.append({"Date": date_val, "Daily Return": row["Daily Return"]})
            results = filtered
        daily_ret_graph = visualization.plot_daily_ret(results)

    return render_template("daily_ret.html", results = results, start_date = start_date, end_date = end_date, daily_ret_graph= daily_ret_graph)



if __name__ == "__main__":
    app.run(debug=True)



#references
#https://www.w3schools.com/python/default.asp
#https://en.wikipedia.org/wiki/Moving_average
#https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp
#https://docs.python.org/3/library/csv.html
#https://www.geeksforgeeks.org/python/flask-http-methods-handle-get-post-requests/
#https://plotly.com/python/line-and-scatter/#linear-regression-and-other-trendlines