import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import yfinance as yf
import matplotlib.pyplot as plt
import numpy as np

start_date = "2024-04-22"
end_date = "2025-04-23"

def get_stock_data(ticker_symbol, start_str, end_str):
    """
    Fetches historical stock data for a given ticker and date range.

    Args:
        ticker_symbol (str): The stock ticker symbol (e.g., "18MF.DE").
        start_str (str): The start date in YYYY-MM-DD format.
        end_str (str): The end date in YYYY-MM-DD format.

    Returns:
        DataFrame: Historical stock data.
    """
    ticker = yf.Ticker(ticker_symbol)
    curr = ticker.info["currency"]
    if curr != "EUR":
        print(f"Warning: {ticker_symbol} is not in EUR, it is in {curr}")
        exit(1)
    
    hist = ticker.history(start=start_str, end=end_str)
    return hist


start_date = datetime.strptime(start_date, "%Y-%m-%d")
end_date = datetime.strptime(end_date, "%Y-%m-%d")

labels = ["iShares Ultrashort Bond", "Invesco Euro Cash 3 Months", "Xtrackers II EUR Overnight Rate Swap", "Amundi Prime Euro Government Bonds"]
tickers = ["ERNX.DE", "PJEU.DE", "XEON.DE", "PRAB.DE"]



file_path = "bundesschatz_combined.csv"
bundesschatz_data = pd.read_csv(file_path)

bs1m_data = bundesschatz_data[bundesschatz_data["Product Key"] == "BS1M"]
bs1m_data = bs1m_data[["Date", "Interest Rate"]]
bs1m_data["Date"] = pd.to_datetime(bs1m_data["Date"])

bs6m_data = bundesschatz_data[bundesschatz_data["Product Key"] == "BS6MG"]
bs6m_data = bs6m_data[["Date", "Interest Rate"]]
bs6m_data["Date"] = pd.to_datetime(bs6m_data["Date"])



bs1m = [[start_date], [1]]
bs1m_interest = bs1m_data.loc[bs1m_data["Date"] <= start_date, "Interest Rate"].iloc[-1]
bs6m = [[start_date], [1]]
bs6m_interest = bs6m_data.loc[bs6m_data["Date"] <= start_date, "Interest Rate"].iloc[-1]

current_date = start_date
bs1m_start = start_date
bs6m_start = start_date
while current_date <= end_date:
    current_date += timedelta(days=1)
    difference = relativedelta(current_date, start_date)

    bs1m[0].append(current_date)
    if difference.days == 0 and (difference.months > 0 or difference.years > 0):
        days = (current_date - bs1m_start).days
        bs1m[1].append(bs1m[1][-1] * (1 + bs1m_interest / 100 * days / 365))
        bs1m_start = current_date
        bs1m_interest = bs1m_data.loc[bs1m_data["Date"] <= current_date, "Interest Rate"].iloc[-1]
    else:
        bs1m[1].append(bs1m[1][-1])


    bs6m[0].append(current_date)
    if difference.days == 0 and (difference.months == 6 or (difference.months == 0 and difference.years > 0)):
        days = (current_date - bs6m_start).days
        bs6m[1].append(bs6m[1][-1] * (1 + bs6m_interest / 100 * days / 365))
        bs6m_start = current_date
        bs6m_interest = bs6m_data.loc[bs6m_data["Date"] <= current_date, "Interest Rate"].iloc[-1]
    else:
        bs6m[1].append(bs6m[1][-1])


bs1m = np.array(bs1m)
bs6m = np.array(bs6m)

plt.figure(figsize=(10, 6))

# Loop through tickers and labels to fetch data and plot
for ticker, label in zip(tickers, labels):
    price_data = get_stock_data(ticker, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))
    plt.plot(price_data.index, ((price_data['Close']/price_data['Close'][0]) - 1)*100, label=label)



plt.plot(bs1m[0], (bs1m[1] - 1) * 100, label="Bundesschatz 1 Monat", color="black", linestyle="--")
plt.plot(bs6m[0], (bs6m[1] - 1) * 100, label="Bundesschatz 6 Monate", color="red", linestyle="--")

# Customize the plot
plt.title("Closing Prices for Multiple Tickers")
plt.xlabel("Datum")
plt.ylabel("Bruttorendite (%)")
plt.legend()
plt.grid()
plt.show()