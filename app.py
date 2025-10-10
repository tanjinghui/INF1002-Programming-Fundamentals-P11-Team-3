from flask import Flask, render_template, request
from datetime import datetime,timedelta
import csv
import functions
import visualization
import yfinance as yf

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


def setupTickers(listOfTickers: list[str], start_date: str, end_date: str) -> dict[str:dict]:
    """
    Download stock data for given tickers and date range using yfinance.

    assume: start_date, end_date format: "YYYY-MM-DD"

    listOfTickers: a list of strings where each string is a valid 3/4 letter ticker on real stock markets
    start_date: a string in format YYYY-MM-DD to indicate which day to start from
    end_date: a string in format YYYY-MM-DD to indicate which day to end at

    return: a nested dictionary with the ticker as the key. e.g. {"AAPL":{"Date":..., "Close":..., ...}, "META":{...}}

    references:
    https://stackoverflow.com/questions/25852044/converting-pandas-tslib-timestamp-to-datetime-python
    """
    try:
        result = {}
        data = yf.download(listOfTickers, start = start_date, end = end_date, auto_adjust=True, progress=False)
        for ticker in listOfTickers:
            # -------------------------------------------
            # get datetime obj for indexing like CSV loading function
            # -------------------------------------------
            dates = [date.to_pydatetime() for date in data.index]
            # -------------------------------------------
            # use list comprehension to retrieve and process data into correct type
            # -------------------------------------------
            close_prices = [float(close) for date,close in data["Close"][ticker].items()]
            volume = [int(vol) for date,vol in data["Volume"][ticker].items()]
            open_price = [float(open) for date,open in data["Open"][ticker].items()]
            high_price = [float(high) for date,high in data["High"][ticker].items()]
            low_price = [float(low) for date,low in data["Low"][ticker].items()]
            # -------------------------------------------
            # Combine the data together by index in order to sort all data together by date
            # Unpacks the data into their respective lists
            # -------------------------------------------
            combineSort = sorted(zip(dates, close_prices, volume, open_price, high_price, low_price), key = lambda dates: dates[0])
            dates, close_prices, volume, open_price, high_price, low_price = zip(*combineSort)
            result[ticker] = {"Date" : list(dates), "Close/Last" : list(close_prices), "Volume" : list(volume), "Open" : list(open_price), "High" : list(high_price), "Low" : list(low_price)}
        return result
    # -------------------------------------------
    # Execption handling in case unable to reach servers
    # -------------------------------------------
    except Exception as e:
        print("Error in setupTickers:", e)
        return None



listOfTickers = ["AAPL" ,"MSFT" ,"GOOG" ,"NVDA" ,"AMZN", "TSLA", "META"]
csvData = loadData("data/apple.csv")
stockData = setupTickers(listOfTickers, "2022-01-01", "2025-10-01")
segmentTrees = {}
if stockData:
    stockData["LOCAL"] = csvData
    for ticker in listOfTickers + ["LOCAL"]:
        segmentTrees[ticker] = functions.SegmentTree(stockData[ticker]["Close/Last"])
else:
    print("Something went horribly wrong in loading of data. Abort Abort Abort")
    raise SystemExit


@app.route("/", methods = ["GET"])
def home():
    source = request.args.get("source", "NVDA")
    date_filter = request.args.get("date_filter", "30")
    if date_filter.lower() != "all":
        try:
            date_filter = int(date_filter)
        except ValueError:
            # Default to 30 if conversion fails
            date_filter = 30
    indexGraph = visualization.plot_indexGraph(stockData[source], source, date_filter)
    return render_template("index.html", indexGraph = indexGraph, source = source, date_filter = date_filter)


@app.route("/range", methods = ["GET", "POST"])
def rangePage():
    # -------------------------------------------
    # Initialize range page
    # -------------------------------------------
    start_date = None
    end_date = None
    average = None
    max_value = None
    source = None
    errorMsg = None
    rows = None
    # -------------------------------------------
    # Get values from form
    # -------------------------------------------
    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        source = request.form.get("source")
        # -------------------------------------------
        # Dates are passed to binary search function to get index
        # Passes values to segment tree to get average and max
        # -------------------------------------------
        if source in listOfTickers + ["LOCAL"]:
            start_date_index = functions.binary_search(stockData[source]["Date"], start_date, direction = 0)
            end_date_index = functions.binary_search(stockData[source]["Date"], end_date, direction = 1)
            average = segmentTrees[source].range_average(start_date_index, end_date_index)
            max_value = segmentTrees[source].range_max(start_date_index, end_date_index)
            dates = stockData[source]["Date"][start_date_index:end_date_index + 1]
            close_prices = stockData[source]["Close/Last"][start_date_index:end_date_index + 1]
            rows = zip(dates, close_prices)
        else:
            errorMsg = "Error: Invalid stock ticker selected."
            return render_template("range.html", start_date = start_date, end_date = end_date, average = average, max_value = max_value, errorMsg = errorMsg, source = source, rows = rows)
    return render_template("range.html", start_date = start_date, end_date = end_date, average = average, max_value = max_value, errorMsg = errorMsg, source = source, rows = rows)


@app.route("/sma", methods = ["GET", "POST"])
def smaPage():
    # -------------------------------------------
    # Initialize sma page
    # -------------------------------------------
    results = None
    start_date = None
    end_date = None
    days_window = None
    maGraph = None
    source = None
    errorMsg = None
    # -------------------------------------------
    # Get values from form
    # -------------------------------------------
    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        days_window = int(request.form.get("days_window"))
        source = request.form.get("source")
        # -------------------------------------------
        # Calls moving average function to get results
        # -------------------------------------------
        if source in listOfTickers + ["LOCAL"]:
            results = functions.moving_average(stockData[source], start_date, end_date, days_window)
        else:
            errorMsg = "Error: Invalid stock ticker selected."
            return render_template("sma.html", results = results, days_window = days_window, start_date = start_date, end_date = end_date, maGraph = maGraph, errorMsg = errorMsg, source = source)
        # -------------------------------------------
        # Call visualisation function to draw graph
        # -------------------------------------------
        try:
            maGraph = visualization.plot_maGraph(results, days_window, source)
        except Exception as e:
            return render_template("sma.html", results = results, days_window = days_window, start_date = start_date, end_date = end_date, maGraph= None, errorMsg = e, source = source)

    return render_template("sma.html", results = results, days_window = days_window, start_date = start_date, end_date = end_date, maGraph= maGraph, source = source)


@app.route("/trend", methods = ["GET", "POST"])
def trendPage():
    # -------------------------------------------
    # Initialise base page ready for ajax
    # -------------------------------------------
    return render_template("trend.html", results = None, trend_window = None, stert_date = None, end_date = None, trendGraph= None, errorMsg=None, bullOrBear = None)

@app.route("/trend_partial", methods=['POST'])
def trend_partial():
    # -------------------------------------------
    # Get values from form
    # -------------------------------------------
    params = {
        "source" : request.values.get("source"),
        "start_date" : request.values.get("start_date"),
        "end_date" : request.values.get("end_date"),
        "trend_window" : request.values.get("trend_window")
    }
    results = None
    trendGraph = None
    start_date = datetime.strptime(params["start_date"], "%Y-%m-%d")
    end_date = datetime.strptime(params["end_date"], "%Y-%m-%d")
    trend_window = int(params["trend_window"])
    source = params["source"]
    # -------------------------------------------
    # look for source in list of tickers to generate graph
    # -------------------------------------------
    if source in listOfTickers + ["LOCAL"]:
        results = functions.trend_finder(stockData[source], start_date, end_date, trend_window)
    else:
        # -------------------------------------------
        # execption handling for unexpected case
        # -------------------------------------------
        errorMsg = "Error: Invalid stock ticker selected."
        return render_template("trend_partial.html", results = None, trend_window = None, stert_date = start_date, end_date = end_date, trendGraph= None, errorMsg=errorMsg, bullOrBear = None)
    # -------------------------------------------
    # Call visualisation function to draw graph
    # -------------------------------------------
    try:
        trendGraph = visualization.plot_updown_trend(results)
    except Exception as e:
        return render_template("trend_partial.html", results = None, trend_window = None, stert_date = start_date, end_date = end_date, trendGraph= None, errorMsg=e, bullOrBear = None)
    return render_template("trend_partial.html", results = results, trend_window = trend_window, stert_date = start_date, end_date = end_date, trendGraph= trendGraph, errorMsg=results[2], bullOrBear = results[3])

@app.route("/max_profit", methods = ["GET", "POST"])
def max_profit_Page():
    results = None
    start_date = None
    end_date = None
    max_profit_Graph = None
    source = None
    if request.method == "POST":
        try:
            start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
            end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
            source = request.form.get("source")
            if source in listOfTickers + ["LOCAL"]:
                results = functions.max_profit(stockData[source], start_date, end_date)
            else:
                errorMsg = "Error: Invalid stock ticker selected."
                return render_template("max_profit.html", results = None, stert_date = start_date, end_date = end_date, max_profit_Graph= None, errorMsg=errorMsg)
            max_profit_Graph = visualization.plot_max_profit(stockData[source],results)
            return render_template("max_profit.html", results = results, stert_date = start_date, end_date = end_date, max_profit_Graph= max_profit_Graph, errorMsg=results[4])
        except Exception as e:
            return render_template("max_profit.html", results = None, stert_date = start_date, end_date = end_date, max_profit_Graph= None, errorMsg=e)
    return render_template("max_profit.html", results = None, stert_date = start_date, end_date = end_date, max_profit_Graph= None, errorMsg=None)


@app.route("/daily_return", methods = ["GET", "POST"])
def daily_return_Page():
    # -------------------------------------------
    #initialize base page ready for ajax
    # -------------------------------------------
    results = None
    start_date = None
    end_date = None
    daily_ret_graph = None
    source = None
    # -------------------------------------------
    # Get values from form
    # -------------------------------------------
    if request.method == "POST":
        start_date = datetime.strptime(request.form.get("start_date"), "%Y-%m-%d")
        end_date = datetime.strptime(request.form.get("end_date"), "%Y-%m-%d")
        source = request.form.get("source")
        if source in listOfTickers + ["LOCAL"]:
            results = functions.daily_ret(stockData[source])
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
        else:
            errorMsg = "Error: Invalid stock ticker selected."
            return render_template("daily_ret.html", results = None, start_date = start_date, end_date = end_date, daily_ret_graph= None)
            # -------------------------------------------
            # Call visualisation function to draw graph
            # -------------------------------------------
        try:
            daily_ret_graph = visualization.plot_daily_ret(results, source)
        except Exception as e:
            return render_template("daily_ret.html", results = None, start_date = start_date, end_date = end_date, daily_ret_graph= None)

    return render_template("daily_ret.html", results = results, start_date = start_date, end_date = end_date, daily_ret_graph= daily_ret_graph)



if __name__ == "__main__":
    app.run(debug=True)
