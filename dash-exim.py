# the dash app for import export

import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

ex = pd.read_csv('2018-2010_export.csv')
im = pd.read_csv('2018-2010_import.csv')

story = '''India exports approximately 7500 commodities to about 190 countries, and imports around 6000 
commodities from 140 countries. India exported US$318.2 billion and imported $462.9 billion 
worth of commodities in 2014. The Government of India's Economic Survey 2017-18 noted that 
five states — Maharashtra, Gujarat, Karnataka, Tamil Nadu and Telangana — accounted for 
70% of India's total exports. It was the first time that the survey included international 
export data for states. The survey found a high correlation between a state's 
Gross State Domestic Product (GSDP) per capita and its share of total exports. 
With a high GSDP per capita but low export share, Kerala was the only major outlier 
because the state's GSDP per capita was heavily influenced by remittances. 
The survey also found that the largest firms in India contributed to a smaller 
percentage of exports when compared to countries like Brazil, Germany, Mexico, and the United States. 
The top 1% of India's companies accounted for 38% of total exports.'''

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.5/css/bulma.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Import Export Dash'

app.layout = html.Section([
    html.P('Import and Export Visualization',
    className = "title has-text-centered"),
    html.Div([
        html.Div(story, className = "subtitle has-text-justified column"),
        html.Div([
            dcc.Graph(
                            id="total-exim",
                            figure={
                                'data': [{
                                    'x': [i for i in np.unique(ex.year)],
                                    'y': im.groupby('year').agg(np.sum).value,
                                    'type': 'bar',
                                    'name': 'Imports'
                                },
                                    {
                                    'x': [i for i in np.unique(ex.year)],
                                    'y': ex.groupby('year').agg(np.sum).value,
                                    'type': 'bar',
                                    'name': 'Exports'
                                }
                                ],
                                'layout': {
                                    'title': 'Imports and Exports of India from 2010 to 2018',
                                    'xaxis': {
                                        'title': 'Countries'
                                    },
                                    'yaxis': {
                                        'title': 'Million INR'
                                    }
                                }
                            }
                        )
        ], className = "column"),
    ],
    className = "columns"),
    html.Div([
        html.Div([
            dcc.Dropdown(
                            id='yearInput',
                            options=[{'label': i, 'value': i}
                                     for i in np.unique(ex.year)],
                            value=2018
                        )
        ],
        className = "column is-one-third")
    ], className = "columns is-centered" ),
    html.Div([
        html.Div([
                        dcc.Graph(
                            id='outputGraphImport'
                        ),
                    ], className="column"),
                    html.Div([
                        dcc.Graph(
                            id='outputGraphExport'
                        )
                    ], className="column")
    ],
    className = "columns")
],
className = "container")

@app.callback(
    Output('outputGraphImport', 'figure'),
    [Input('yearInput', 'value')])
def im_update_figure(yearInput):
    df_im = im[im.year == yearInput]
    figure = {
        'data': [{
            "x": df_im.groupby('country').sum().sort_values(by=['value'], ascending=False).head(7).index,
            "y":df_im.groupby('country').sum().sort_values(by=['value'], ascending=False).value.head(7),
            "type":'bar',
        }],
        'layout': {
            'title': 'Imports to India for the selected year',
            'xaxis': {
                'title': 'Countries'
            },
            'yaxis': {
                'title': 'INR (Million)'
            }
        }}
    return figure


@app.callback(
    Output('outputGraphExport', 'figure'),
    [Input('yearInput', 'value')])
def ex_update_figure(yearInput):
    df_ex = ex[ex.year == yearInput]
    figure = {
        'data': [{
            "x": df_ex.groupby('country').sum().sort_values(by=['value'], ascending=False).head(7).index,
            "y":df_ex.groupby('country').sum().sort_values(by=['value'], ascending=False).value.head(7),
            "type":'bar',
        }],
        'layout': {
            'title': 'Exports from India for the selected year',
            'xaxis': {
                'title': 'Countries'
            },
            'yaxis': {
                'title': 'INR (Million)'
            }
        }}
    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
