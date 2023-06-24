from dash import Dash, dcc, html, Input, Output, exceptions
import plotly.graph_objects as go
import plotly.figure_factory as ff
import binance_data 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from datetime import datetime as dt
import numpy as np
import scipy.stats as stats
from scipy.stats import johnsonsu

# Download data
bd = binance_data.BinanceData()

df = {
    'ETHUSDT': bd.get_data('ETHUSDT'),
    'BTCUSDT': bd.get_data('BTCUSDT')
}

# Upload template 
load_figure_template('SLATE')
external_stylesheets = [dbc.themes.SLATE]

# Build the figures
sidebar = html.Div(
    [
        html.H4("Filters"),
        html.Hr(),   
        dbc.Nav(
            [
                html.Div([
                    html.P("Select an asset:", className="filter_label"),
                    dbc.Select(
                    id="dropdown-select-asset",
                    options=[
                        {'label': 'ETHUSDT', 'value': 'ETHUSDT'},
                        {'label': 'BTCUSDT', 'value': 'BTCUSDT'}],
                    value='ETHUSDT',                                   
                )
                ]),
                html.Br(),
                html.Div([
                    html.P("Type of graph:", className="filter_label"),
                    dbc.RadioItems(
                    id="type-of-graph",
                    options=[
                        {'label': 'Candlestick Chart', 'value': 'candlestick'},
                        {'label': 'Return Histogram', 'value': 'histogram'},
                        {'label': 'Comparative Returns', 'value': 'comparative'}],
                    value='candlestick',
                    class_name="mb-3 custom-select"                                    
                )
                ]),                  
            ],
            vertical=True,
            pills=True,
        ),
    ],
    className="sidebar"
)

date_picker_ranger = dcc.DatePickerRange(
    id='date-picker-range',
    min_date_allowed=df[list(df.keys())[0]].index[0],
    max_date_allowed=df[list(df.keys())[0]].index[-1],
    className="custom-date-picker")

reset_button = dbc.Button(
    html.Img(src='/assets/reset_icon.png', 
             style={'width': '20px', 'height': '20px'}), 
    className="reset-button-img",
    id='reset-button', 
    n_clicks=0,
    color = 'transparent',
    size = 'sm')

rangeslider = dcc.Checklist(
    id='toggle-rangeslider',
    options=[{'label': 'Include Rangeslider',
              'value': 'slider'}],
    value=['slider'],
    style={'position': 'absolute', 'right': '80px', 'z-index': '999'})

card_content_left = [
    dbc.CardHeader("Descriptive Statistics"),
    dbc.CardBody(id='descriptive-stats', style={'line-height': '0.75'})]

card_content_right = [
    dbc.CardHeader("Value at Risk (VaR) Model"),
    dbc.CardBody(
        [
        dcc.Markdown(
                '''
                Value at risk (VaR) is a statistic measure that quantifies the extent of possible 
                financial losses within a portfolio. In this model, we calculate the VaR 
                using three different methods: historical and parametrical (Normal and Johnson SU distribution).
                It represents the maximum loss with a probability of 95% (confidence level) on a daily return basis.
                '''
            ),
        html.P(id='var-model', style={'line-height': '0.75'})
        ])
]

card_row = dbc.Row([
    dbc.Col(dbc.Card(card_content_left, color="dark", outline=True)),
    dbc.Col(dbc.Card(card_content_right, color="dark", outline=True),
            style={'marginRight': '200px'})
    ],
    id='bottom-row')

def calculate_var(returns, confidence_level=0.05):
    var_hist = np.percentile(returns, 100 * confidence_level)
    mean = np.mean(returns)
    std_dev = np.std(returns)
    z = stats.norm.ppf(confidence_level)
    var_normal = mean - std_dev * z
    params = johnsonsu.fit(returns)
    dist = johnsonsu(*params)
    var_js = dist.ppf(confidence_level)
    return var_hist, var_normal, var_js

# Create the layout
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Crypto Dashboard"

app.layout = html.Div([
                dbc.Row([
                    dbc.Col(className="banner", 
                            children=[html.H2(
                                html.A('Crypto Dashboard',
                                       href='https://github.com/lucianaveron/crypto_dashboard')
                                       )]
                            ),
                    dbc.Col()                                 
                    ]),
                dbc.Row(
                    [dbc.Col(sidebar, width=2),
                    dbc.Col([
                        html.Div([date_picker_ranger,
                                  reset_button                                
                        ], style={'position': 'absolute', 'right': '80px', 'z-index': '999'}),

                        dcc.Graph(id='graph', style={'marginTop': '-30px', 'marginBottom': '-50px'}),
                        rangeslider, 
                        card_row   
                    ])
                ])                    
])

@app.callback(
    Output('date-picker-range', 'start_date'),
    Output('date-picker-range', 'end_date'),
    Input('reset-button', 'n_clicks')
)
def reset_date_picker(n_clicks):
    if n_clicks > 0:
        return df[list(df.keys())[0]].index[0], df[list(df.keys())[0]].index[-1]
    else:
        raise exceptions.PreventUpdate
    
@app.callback(
    Output('graph', 'figure'),
    Input('dropdown-select-asset', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input('toggle-rangeslider', 'value'),
    Input('type-of-graph', 'value'))
def update_figure(selected_asset, start_date, end_date, slider, graph_type):
    filtered_df = df[selected_asset]
    if start_date and end_date:
        filtered_df = filtered_df.loc[(filtered_df.index >= start_date) & (filtered_df.index <= end_date)]
    
    if graph_type == 'candlestick':
        fig = go.Figure(data=[go.Candlestick(
            x=filtered_df.index,
            open=filtered_df['Open'],
            high=filtered_df['High'],
            low=filtered_df['Low'],
            close=filtered_df['Close'])])
        fig.update_layout(transition_duration=500,
                          xaxis_rangeslider_visible='slider' in slider,
                          height=600,
                          title=f'{selected_asset} Candlestick Chart'
                          )
    elif graph_type == 'histogram':
        returns = (np.log(filtered_df['Close']/filtered_df['Close'].shift(1))*100).dropna()
        mu, sigma = stats.norm.fit(returns)
        x = np.linspace(min(returns), max(returns), len(returns))
        y = stats.norm.pdf(x, mu, sigma)

        a, b, loc, scale = johnsonsu.fit(returns)
        x_js = np.linspace(min(returns), max(returns), 100)
        y_js = johnsonsu.pdf(x_js, a, b, loc, scale)

        fig = go.Figure()
        fig.add_trace(go.Histogram(x=returns, nbinsx=50, histnorm='probability density',
                                   opacity=0.75, name='Logarithmic Returns'))
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', name='Normal Distribution'))
        fig.add_trace(go.Scatter(x=[mu - sigma, mu - sigma], y=[0, max(y)], mode='lines', name='-1 Std Dev', line=dict(color='red')))
        fig.add_trace(go.Scatter(x=[mu + sigma, mu + sigma], y=[0, max(y)], mode='lines', name='+1 Std Dev', line=dict(color='red')))
        
        fig.add_trace(go.Scatter(x=x_js, y=y_js,
                                  mode='lines', name='Johnsonsu Distribution'))
        
        fig.update_layout(transition_duration=500,
                            height=600,
                            title=f'{selected_asset} Daily Log Return Histogram (in %)')
        
    elif graph_type == 'comparative':
        returns = [(np.log(filtered_df['Close']/filtered_df['Close'].shift(1))*100).dropna()]
        fig = ff.create_distplot(returns,
        group_labels=['Log Return (in %)'])
        fig.update_layout(transition_duration=500,
                            height=600,
                            title=f'{selected_asset} Return Histogram 2222')
    else:
        raise exceptions.PreventUpdate

    return fig

@app.callback(
    Output('toggle-rangeslider', 'style'),
    Input('type-of-graph', 'value'))
def update_slider_visibility(graph_type):
    if graph_type == 'candlestick':
        return {'position': 'absolute', 'right': '80px', 'z-index': '999'}
    else:
        return {'display': 'none'}
    
@app.callback(
    Output('bottom-row', 'style'),
    Input('type-of-graph', 'value'))
def update_bottom_row_visibility(graph_type):
    if graph_type == 'histogram':
        return {'right': '100px', 'z-index': '999'}
    else:
        return {'display': 'none'}
    
@app.callback(
    Output('descriptive-stats', 'children'),
    Output('var-model', 'children'),
    Input('dropdown-select-asset', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
)
def update_card_content(selected_asset, start_date, end_date):
    filtered_df = df[selected_asset]
    if start_date and end_date:
        filtered_df = filtered_df.loc[(filtered_df.index >= start_date) & (filtered_df.index <= end_date)]
    
    returns = np.log(filtered_df['Close']/filtered_df['Close'].shift(1)).dropna()
    var_hist, var_normal, var_js = calculate_var(returns)
    return [[html.P(f'Average Daily Return: {round(returns.mean()*100, 2)}%'),
            html.P(f'Standard Deviation: {round(returns.std()*100, 2)}%'),
            html.P(f'Minimum Daily Return: {round(returns.min()*100, 2)}%'),
            html.P(f'Maximum Daily Return: {round(returns.max()*100, 2)}%'),
            html.P(f'Number of Observations: {len(returns)}')],
            [html.P(f'Historical VaR (95%): {round(var_hist*100, 2)}%'),
            html.P(f'Normal VaR (95%): {round(var_normal*100, 2)}%'),
            html.P(f'Johnsonsu VaR (95%): {round(var_js*100, 2)}%')
            ]]


if __name__ == '__main__':
    app.run(debug=True)
