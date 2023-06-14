from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import binance_data 
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

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
SIDEBAR_STYLE = {  
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#272b30",
}

sidebar = html.Div(
    [
        html.H2("Filters"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with filters", className="lead"
        ),
        dbc.Nav(
            [
                dcc.Dropdown(id = 'dropdown',
                             options=[
                                 {'label': 'ETHUSDT', 'value': 'ETHUSDT'},
                                 {'label': 'BTCUSDT', 'value': 'BTCUSDT'}],
                                 value='ETHUSDT'),
                html.Br(),
                dcc.Dropdown(id = 'two'),
                html.Br(),
                dcc.Dropdown(id = 'three'),
                html.Br(),
                dcc.Checklist(id='toggle-rangeslider',
                              options=[{'label': 'Include Rangeslider',
                                        'value': 'slider'}],
                                        value=['slider'])

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


# Create the layout
app = Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
                dbc.Row([
                    dbc.Col(),
                    dbc.Col(html.H1('Binance Data'),width = 10, style = {'margin-left':'7px','margin-top':'7px'})
                    ]),
                dbc.Row(
                    [dbc.Col(sidebar),
                    dbc.Col(dcc.Graph(id = 'graph'), width = 10, style = {'margin-left':'15px', 'margin-top':'7px', 'margin-right':'15px'})
                    ])
    ]
)


@app.callback(
    Output('graph', 'figure'),
    Input('dropdown', 'value'),
    Input("toggle-rangeslider", "value"))
def update_figure(selected_asset, slider):
    filtered_df = df[selected_asset]
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
