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
            print(f"{ticker}: לא נמצא מיד
