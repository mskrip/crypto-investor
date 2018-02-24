#!/usr/bin/env python
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from datetime import datetime as dt
from pandas_datareader import data as web


app = dash.Dash()


def serve_layout():
    return html.H1('The time is: {}'.format(str(dt.now())))


app.layout = html.Div([
    serve_layout(),
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'Coke', 'value': 'COKE'},
            {'label': 'Tesla', 'value': 'TSLA'},
            {'label': 'Apple', 'value': 'AAPL'}
        ],
        value='COKE'
    ),
    dcc.Graph(id='my-graph')
])


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    df = web.DataReader(
        selected_dropdown_value, data_source='google',
        start=dt(2017, 1, 1), end=dt.now()
    )
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }]
    }


if __name__ == '__main__':
    app.run_server(debug=True)
