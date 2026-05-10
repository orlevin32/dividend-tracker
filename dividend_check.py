import requests
import json
import os

API_KEY = "wFkifHunSas5JwNh8CPzejxMjDW4mdsb"
BASE_URL = "https://financialmodelingprep.com/api/v3"
MEMORY_FILE = "dividend_memory.json"

def get_latest_dividend(ticker):
    url = f"{BASE_URL}/historical/stock_dividend/{ticker}?apikey={API_KEY}&limit=1"
    response = requests.get(url)
    data = response.json()
    history = data.get("historical", [])
    if history:
        return history[0]
    return None

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def check_dividends():
    with open("stocks.json", "r") as f:
        stocks = json.load(f)["stocks"]

    memory = load_memory()
    alerts = []

    for ticker in stocks:
        latest = get_latest_dividend(ticker)

        if not latest:
            print(ticker + ": no data found")
            continue

        latest_amount = latest["dividend"]
        latest_date = latest["date"]

        print(ticker + ": " + str(latest_amount) + " date: " + latest_date)

        if ticker in memory:
            previous_amount = memory[ticker]["amount"]
            previous_date = memory[ticker]["date"]

            if latest_date != previous_date:
                if latest_amount < previous_amount:
                    alerts.append({
                        "ticker": ticker,
                        "latest": latest_amount,
                        "previous": previous_amount,
                        "date": latest_date
                    })
                memory[ticker] = {"amount": latest_amount, "date": latest_date}
        else:
            memory[ticker] = {"amount": latest_amount, "date": latest_date}
            print(ticker + ": saved to memory")

    save_memory(memory)

    if alerts:
        print("ALERT - dividend cut detected:")
        for alert in alerts:
            print(alert["ticker"] + " | date: " + alert["date"] + " | previous: " + str(alert["previous"]) + " | new: " + str(alert["latest"]))
    else:
        print("OK - no dividend cuts detected")

if __name__ == "__main__":
    check_dividends()
