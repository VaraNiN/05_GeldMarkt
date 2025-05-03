import requests
from datetime import datetime
import yfinance as yf
import matplotlib.pyplot as plt

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


# Example usage:
labels = ["iShares Ultrashort Bond", "Invesco Euro Cash 3 Months", "Xtrackers II EUR Overnight Rate Swap", "Amundi Prime Euro Government Bonds"]
tickers = ["ERNX.DE", "PJEU.DE", "XEON.DE", "PRAB.DE"]
start_date = "2024-04-22"
end_date = datetime.now().strftime("%Y-%m-%d")

plt.figure(figsize=(10, 6))

# Loop through tickers and labels to fetch data and plot
for ticker, label in zip(tickers, labels):
    price_data = get_stock_data(ticker, start_date, end_date)
    plt.plot(price_data.index, ((price_data['Close']/price_data['Close'][0]) - 1)*100, label=label)

# Customize the plot
plt.title("Closing Prices for Multiple Tickers")
plt.xlabel("Date")
plt.ylabel("Change (%)")
plt.legend()
plt.grid()
plt.show()