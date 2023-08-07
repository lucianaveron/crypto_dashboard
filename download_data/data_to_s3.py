import binance_data 
import boto3

bd = binance_data.BinanceData()

asset_list = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'XRPUSDT', 'ADAUSDT', 'DOGEUSDT', 'TRXUSDT', 'SOLUSDT', 'LTCUSDT', 'DOTUSDT', 
              'MATICUSDT', 'BCHUSDT', 'AVAXUSDT', 'SHIBUSDT','LINKUSDT', 'ATOMUSDT', 'XMRUSDT', 'UNIUSDT', 'VETUSDT', 'FILUSDT']
            
s3_client = boto3.client('s3')

bucket_name = 'cryptobucketbinance'

for asset in asset_list:
    df = bd.get_data_thread(asset, '1d', '2017-08-01')
    df.to_csv(f"s3://{bucket_name}/{asset}.csv")
