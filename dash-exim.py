#the dash app for import export

import pandas as pd
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objects as go

ex = pd.read_csv('2018-2010_export.csv')
im = pd.read_csv('2018-2010_import.csv')

story = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec imperdiet elit at urna varius, non sagittis augue porttitor. Vestibulum felis mauris, dignissim ac convallis ac, dapibus nec neque. Ut convallis metus vel ipsum consectetur scelerisque. Sed elementum eget nunc a maximus. Vestibulum accumsan lorem eros, vitae placerat mi consectetur nec. Morbi tortor eros, lobortis nec dolor a, aliquet interdum ex. In erat felis, placerat iaculis pellentesque nec, bibendum dictum ex. Etiam vitae ipsum vestibulum lectus viverra vulputate. Nulla nisi risus, iaculis a tortor sit amet, hendrerit volutpat nisi. Aenean tempor pretium nisl, vitae mattis ipsum facilisis quis. Ut ultricies, dolor at viverra pharetra, mauris purus gravida urna, id faucibus felis est eget massa. Nam viverra nibh et metus ultricies tempus. Donec quis enim vel tortor consectetur fermentum. Phasellus maximus enim nec posuere venenatis. Curabitur ac tincidunt erat, et porta enim. Sed pulvinar blandit dolor et vulputate. Cras tristique diam dui, in pulvinar turpis convallis nec. Vivamus egestas mattis tellus sed lacinia."

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/bulma/0.7.5/css/bulma.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = 'Import Export Dash'

app.layout = html.Div([
    html.H1(
        'Import and Exports of India from 2010 to 2018',
        className="title has-text-centered"),  # class for title
    html.Div([  # container division for main content
        html.Div([  # left division
            html.P(
                story,
                className="subtitle"  # class for para in left division
            ),
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
        ],
            className="column"),  # class for left division
        html.Div([  # right division
            dcc.Dropdown(
                id='yearInput',
                options=[{'label': i, 'value': i} for i in np.unique(ex.year)],
                value=2018
            ),
            dcc.Graph(
                id='outputGraphImport'
            ),
            dcc.Graph(
                id='outputGraphExport'
            )
        ],
            className="column")  # class for right division
    ],
        className="container columns")  # class for container
],
    className="container")  # class for outermost division


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
    app.run_server(debug=False)
