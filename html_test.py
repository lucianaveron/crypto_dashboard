import pandas as pd
import requests  

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px


def download_data(symbol, interval='1d', startTime=None, endTime=None, limit=1000):
    
    url = 'https://api.binance.com/api/v3/klines'
    
    params = {'symbol':symbol, 'interval':interval, 
              'startTime':startTime, 'endTime':endTime, 'limit':limit}
        
    r = requests.get(url, params=params)
    js = r.json()
    
    cols = ['openTime','Open','High','Low','Close','Volume','cTime',
            'qVolume','trades','takerBase','takerQuote','Ignore']
    df = pd.DataFrame(js, columns=cols)
    
    df = df.apply(pd.to_numeric)

    df.index = pd.to_datetime(df.openTime, unit='ms')
    
    df = df.drop(['openTime','cTime','takerBase','takerQuote','Ignore'],axis=1)
    
    return df


df = {
    'ETHUSDT' : download_data('ETHUSDT', interval='1h', limit=1000),
    'BTCUSDT' : download_data('BTCUSDT', interval='1h', limit=1000)
    }


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H2('Binance Data', style={'textAlign':'center'}),
    html.Br(),
    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'ETHUSDT', 'value': 'ETHUSDT'},
            {'label': 'BTCUSDT', 'value': 'BTCUSDT'}
        ],
        value='ETHUSDT'
    ),
    dcc.Graph(id='graph')
])

@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value'))
def update_figure(selected_asset):
    filtered_df = df[selected_asset].Close
    fig = px.line(filtered_df)
    fig.update_layout(transition_duration=500)
    return fig

if __name__ == '__main__':
    app.run(debug=True)

