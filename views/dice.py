import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

import callbacks.dice
from server import app

testlist = ['四川省', '陕西省', '广东省']
options1 = [{'label': item, 'value': item}for item in testlist]

fig = px.scatter(x=range(10), y=range(10), height=400)
fig.update_layout(clickmode='event+select')  # 设置点击模式

dice_page = html.Div(
    [
        html.Br(),
        html.Br(),
        dcc.Interval(id='dice-first-interval', interval=1, max_intervals=1, disabled=False),
        dbc.Container([
            dbc.Row(
                [
                    dbc.Col('Time Dim', width=3),
                    dbc.Col('Area Dim', width=3),
                    dbc.Col('Platform Dim', width=3),
                    dbc.Col('Software Dim', width=3)
                ]
            ),
            dbc.Row(
                [
                    # dbc.Col('Time', width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id='dice-Time-Dim-dropdown',
                            placeholder='Time',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['dice', 'All', '8', '9', '10']
                            ],
                            multi=True
                        ),
                        width=3
                    ),
                    # dbc.Col('Area Dim', width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id='dice-Area-Dim-dropdown',
                            placeholder='Area',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['Central China', 'Southwest', 'East China', 'South China']
                            ],
                            multi=True

                        ),
                        width=3
                    ),
                    # dbc.Col('Platform', width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id='dice-Platform-Dim-dropdown',
                            placeholder='Platform',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['Baidu', 'ZGC', '2345']
                            ],
                            multi=True

                        ),
                        width=3
                    ),
                    # dbc.Col('Software', width=3)
                    dbc.Col(
                        dcc.Dropdown(
                            id='dice-Software-Dim-dropdown',
                            placeholder='Software',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['Kingsoft Antivirus', 'Tencent Manage', '360 Manage', 'Baidu Manage',
                                             '2345HaoZip', 'WinRAR', '360Zip', 'Bandizip', 'QQ Browser', '360 Browser',
                                             'Firefox', 'Chrome']
                            ],
                            multi=True

                        ),
                        width=3
                    ),
                ]
            ),
            html.Br(),
            dbc.Row([dbc.Col(dbc.Button('查询', id='dice-query-button'), width=3),
                     # dbc.Col(dbc.Button('连接', id='dice-connect-button'), width=3),
                     # dbc.Col(dbc.Button('测试', id='dice-test-button'), width=3),
                     dcc.Store(id='dice-query-store-1', storage_type='session'),
                     dcc.Store(id='dice-query-store-2', storage_type='session'),
                     dcc.Store(id='dice-display-flag-store', storage_type='session')]),
            dbc.Row(html.Pre(id='dice-dropdown-output-1',
                    style={'background-color': '#d4d4d420'})),
            dbc.Row(html.Pre(id='dice-connect-output-1',
                    style={'background-color': '#d4d4d420'})),
            dbc.Row(html.Pre(id='dice-test-output-1',
                    style={'background-color': '#d4d4d420'}))
        ]),
        html.Hr(),
        dbc.Container([], id='dice-figure-container'),
        dcc.Graph(figure=fig, id='dice-scatter'),
        html.Hr(),
    ]
)
