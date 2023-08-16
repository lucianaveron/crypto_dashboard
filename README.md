# Crypto Dashboard

## About this app
Click here :point_right: https://crypto-dashboard-caey22wkcq-od.a.run.app

This dashboard allows you to explore diferents cryptocurrencies and its statistics.

First you have to choose one asset, and then the kind of graph you would like to see.
* "Candlestick Chart", where you can change the date filter.
* "Return Histogram", where you can also see some descriptive metrics and the VaR Model through 3 differents methods.
* "Comparative Returns", where you also see a boxplot comparison between the BTC/USDT returns and the asset selected.

## Tools used in the project
In this project I made use of the following tools:

* Creating a dashboard using the library "Dash".
* Download the data from https://binance-docs.github.io/apidocs/ using the library "Requests" and Threading.
* Upload the data to a AWS S3 Bucket.
* As an online dashboard, it is deployed in Google - Cloud Run, which let us Build and deploy scalable containerized apps.


