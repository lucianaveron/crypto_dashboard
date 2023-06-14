import pandas as pd
import requests

class BinanceData:
    def __init__(self):
        self.base_url = 'https://api.binance.com/api/v3/klines'
        self.limit = 1000


    def get_data(self, symbol, interval = '1d', start_time=None, end_time=None):
        params = {'symbol': symbol, 'interval': interval,
                  'startTime': start_time, 'endTime': end_time, 'limit': self.limit}
        r = requests.get(self.base_url, params=params)
        js = r.json()
        cols = ['openTime', 'Open', 'High', 'Low', 'Close', 'Volume', 'cTime',
            'qVolume', 'trades', 'takerBase', 'takerQuote', 'Ignore']
        df = pd.DataFrame(js, columns=cols)
        df = df.apply(pd.to_numeric)
        df.index = pd.to_datetime(df.openTime, unit='ms')
        df = df.drop(['openTime', 'cTime', 'qVolume', 'trades', 'takerBase',
                  'takerQuote', 'Ignore'], axis=1)
        return df

    def get_close_data(self, symbol, interval = '1d', start_time=None, end_time=None):
        df = self.get_data(symbol, interval, start_time, end_time)
        return df['Close']
    
