from dash import Dash, dcc, html, Input, Output, exceptions
import plotly.graph_objects as go
import binance_data 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from datetime import datetime as dt

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
                    class_name="mb-3 custom-select"                                    
                )
                ]),
                html.Br()
                  
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

checklist = dcc.Checklist(
    id='toggle-rangeslider',
    options=[{'label': 'Include Rangeslider',
              'value': 'slider'}],
    value=['slider'],
    style={'position': 'absolute', 'right': '80px', 'z-index': '999'})



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
                        checklist      
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
        # Esta línea se añade para evitar un error de callback al iniciar la aplicación
        raise exceptions.PreventUpdate
    
@app.callback(
    Output('graph', 'figure'),
    Input('dropdown-select-asset', 'value'),
    Input('date-picker-range', 'start_date'),
    Input('date-picker-range', 'end_date'),
    Input("toggle-rangeslider", "value"))
def update_figure(selected_asset, start_date, end_date, slider):
    filtered_df = df[selected_asset]
    if start_date and end_date:
        filtered_df = filtered_df.loc[(filtered_df.index >= start_date) & (filtered_df.index <= end_date)]
    
    fig = go.Figure(data=[go.Candlestick(
                x=filtered_df.index,
                open=filtered_df['Open'],
                high=filtered_df['High'],
                low=filtered_df['Low'],
                close=filtered_df['Close'])])
    fig.update_layout(transition_duration=500,
                      xaxis_rangeslider_visible='slider' in slider,
                      height=600,
                      title=f'{selected_asset} Candlestick Chart',
                      )
    return fig


if __name__ == '__main__':
    app.run(debug=True)
