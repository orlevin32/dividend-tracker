name: Dividend Tracker

on:
  schedule:
    - cron: '0 8 * * 1'  # כל יום ראשון בשעה 8 בבוקר
  workflow_dispatch:  # אפשרות להריץ ידנית

jobs:
  check-dividends:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests
      - name: Run dividend check
        run: python dividend_check.py
