import json
import os
import urllib.request
from datetime import datetime

MEMORY_FILE = "dividend_memory.json"
DATA_FILE = "docs/data.json"

def get_dividend_history(ticker):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range=5y&events=dividends"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read())
        events = data["chart"]["result"][0].get("events", {})
        dividends = events.get("dividends", {})
        if not dividends:
            return []
        sorted_keys = sorted(dividends.keys())
        return [{"amount": dividends[k]["amount"], "date": k} for k in sorted_keys]
    except Exception as e:
        print(ticker + ": error - " + str(e))
        return []

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)

def save_data(output):
    os.makedirs("docs", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(output, f, indent=2)

def check_dividends():
    with open("stocks.json", "r") as f:
        stocks = json.load(f)["stocks"]

    memory = load_memory()
    alerts = []
    output = []

    for ticker in stocks:
        history = get_dividend_history(ticker)

        if not history:
            print(ticker + ": no data found")
            continue

        latest = history[-1]
        latest_amount = latest["amount"]
        latest_date = latest["date"]

        growth = None
        if len(history) >= 5:
            older = history[-5]["amount"]
            if older > 0:
                growth = round(((latest_amount - older) / older) * 100, 1)

        status = "ok"
        if ticker in memory:
            previous_amount = memory[ticker]["amount"]
            previous_date = memory[ticker]["date"]
            if latest_date != previous_date:
                if latest_amount < previous_amount:
                    status = "cut"
                    alerts.append(ticker)
                memory[ticker] = {"amount": latest_amount, "date": latest_date}
        else:
            memory[ticker] = {"amount": latest_amount, "date": latest_date}

        output.append({
            "ticker": ticker,
            "latest_amount": latest_amount,
            "latest_date": latest_date,
            "growth": growth,
            "status": status,
            "history": [h["amount"] for h in history[-8:]]
        })

        print(ticker + ": " + str(latest_amount) + " | growth: " + str(growth) + "%")

    save_memory(memory)
    save_data(output)

    if alerts:
        print("ALERT - dividend cut: " + ", ".join(alerts))
    else:
        print("OK - no dividend cuts detected")

if __name__ == "__main__":
    check_dividends()
