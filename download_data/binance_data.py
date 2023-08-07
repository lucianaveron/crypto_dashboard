import pandas as pd, numpy as np, requests
import datetime as dt, threading

class BinanceData:
    def __init__(self):
        self.base_url = 'https://api.binance.com/api/v3/klines'
        self.limit = 1000

    def date_to_ms(self, date):
        if date != None:
            date_ms = pd.to_datetime(date, format='%Y-%m-%d %H:%M:%S')
            date_ms = int(dt.datetime.timestamp(date_ms))*1000
        else:
            date_ms = None
        return date_ms

    def get_data(self, symbol, interval = '1d', startTime=None, endTime=None):
        '''
        startTime: format='%Y-%m-%d'
        endTime: format='%Y-%m-%d'
        '''    
        startTime = self.date_to_ms(startTime)
        endTime = self.date_to_ms(endTime)
        params = {'symbol': symbol, 'interval': interval,
                  'startTime': startTime, 'endTime': endTime, 'limit': self.limit}
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

    def get_close_data(self, symbol, interval = '1d', startTime=None, endTime=None):
        df = self.get_data(symbol, interval, startTime, endTime)
        return df['Close']
    
    def dates_array(self, startTime=None):
        startTime = pd.to_datetime(startTime)
        endTime = dt.datetime.today()
        dates_array = []
        while startTime < endTime:
            dates_array.append(startTime)
            startTime = startTime + dt.timedelta(hours=1000)
        return dates_array
    
    def get_data_thread(self, symbol, interval = '1d', startTime=None):
        dates_array = self.dates_array(startTime)
        n_threads = len(dates_array)
        subset = np.array_split(dates_array, n_threads)

        dfs = []
        def worker(dates_array):
            for date in dates_array:
                df = self.get_data(symbol, interval, startTime=date)
                dfs.append(df)
            return dfs

        threads = []
        for i in range(n_threads):
            t = threading.Thread(target=worker, args=(subset[i],))
            threads.append(t)
            t.start()
        
        for t in threads:
            t.join()

        df = pd.concat(dfs).drop_duplicates().sort_index()
        df['log_return'] = (np.log(df['Close']/df['Close'].shift(1))*100)
        df.dropna(inplace=True)
        return df

    

    
