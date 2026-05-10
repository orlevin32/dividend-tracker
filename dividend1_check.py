import requests
import json
from datetime import datetime, timedelta

API_KEY = "wFkifHunSas5JwNh8CPzejxMjDW4mdsb"
BASE_URL = "https://financialmodelingprep.com/api/v3"

def get_dividend_history(ticker):
    url = f"{BASE_URL}/historical/stock_dividend/{ticker}?apikey={API_KEY}"
    response = requests.get(url)
    data = response.json()
    return data.get("historical", [])

def check_dividends():
    with open("stocks.json", "r") as f:
        stocks = json.load(f)["stocks"]

    alerts = []

    for ticker in stocks:
        history = get_dividend_history(ticker)

        if len(history) < 2:
            print(f"{ticker}: אין מספיק היסטוריה")
            continue

        latest = history[0]
        previous = history[1]

        latest_amount = latest["dividend"]
        previous_amount = previous["dividend"]

        print(f"{ticker}: דיבידנד אחרון {latest_amount} | קודם {previous_amount}")

        if latest_amount < previous_amount:
            alerts.append({
                "ticker": ticker,
                "latest": latest_amount,
                "previous": previous_amount,
                "date": latest["date"]
            })

    if alerts:
        print("\n🚨 התראות חיתוך דיבידנד:")
        for alert in alerts:
            print(f"""
            ⚠️ {alert['ticker']}
            תאריך הכרזה: {alert['date']}
            דיבידנד קודם: ${alert['previous']}
            דיבידנד חדש: ${alert['latest']}
            """)
    else:
        print("\n✅ הכל תקין – אף מניה לא חתכה דיבידנד")

if __name__ == "__main__":
    check_dividends()
