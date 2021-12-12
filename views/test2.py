import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

import callbacks.test2
testlist = ['四川省', '陕西省', '广东省']
options1 = [{'label': item, 'value': item}for item in testlist]

test2_page = html.Div(
    dbc.Container(
        [
            html.H1('根据省名查询省会城市：'),
            html.Br(),
            html.Br(),
            dcc.Dropdown(
                id='province',
                options=[
                    {'label': '四川省', 'value': '四川省'},
                    {'label': '陕西省', 'value': '陕西省'},
                    {'label': '广东省', 'value': '广东省'}
                ],
                value='四川省'
            ),
            html.P(id='city'),

            dcc.Dropdown(
                id='dropdown-input-1',
                placeholder='单选',
                options=[
                    {'label': item, 'value': item}
                    for item in list('ABCD')
                ],
                style={
                    'width': '300px'
                },
                value='A'
            ),
            html.Pre(id='dropdown-output-1',
                     style={'background-color': '#d4d4d420',
                            'width': '300px'}),
            dcc.Dropdown(
                id='dropdown-input-2',
                placeholder='多选',
                multi=True,
                options=[
                    {'label': item, 'value': item}
                    for item in list('ABCD')
                ],
                style={
                    'width': '300px'
                },
                value='A'
            ),
            html.Pre(id='dropdown-output-2',
                     style={'background-color': '#d4d4d420',
                            'width': '300px'})
        ],
        style={'margin-top': '100px'}
    )
)

