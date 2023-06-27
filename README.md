# Crypto Dashboard

## About this app
This dashboard allows you to explore diferents cryptocurrencies and its statistics.

First you have to choose one asset, and then the kind of graph you would like to see.
* "Candlestick Chart", where you can change the date filter.
* "Return Histogram", where you can also see some descriptive metrics and the VaR Model through 3 differents methods.
* "Comparative Returns", where you also see a boxplot comparison between the BTC/USDT returns and the asset selected.

## How to run this app
I suggest you to create a virtual environment for running this app with Python 3. Clone this repository and open your terminal/command prompt in the root folder.

```bash
git clone https://github.com/lucianaveron/crypto_dashboard
python3 -m virtualenv venv

```

In Unix system:
```bash
source venv/bin/activate
```

In Windows:
```bash
venv\Scripts\activates
```

Install all required packages by running:
```bash
pip install -r requirements.txt
```

Run this app locally with:
```bash
python app.py
```




