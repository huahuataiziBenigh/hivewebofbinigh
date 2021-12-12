import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash_bootstrap_components as dbc

import callbacks.moving
testlist = ['四川省', '陕西省', '广东省']
options1 = [{'label': item, 'value': item}for item in testlist]

fig = px.scatter(x=range(10), y=range(10), height=400)
fig.update_layout(clickmode='event+select')  # 设置点击模式

moving_page = html.Div(
    [
        html.Br(),
        html.Br(),
        dcc.Interval(id='moving-first-interval', interval=1, max_intervals=1, disabled=False),
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
                            id='moving-Time-Dim-dropdown',
                            placeholder='Time',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['moving', 'All', '8', '9', '10']
                            ],

                        ),
                        width=3
                    ),
                    # dbc.Col('Area Dim', width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id='moving-Area-Dim-dropdown',
                            placeholder='Area',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['Central China', 'Southwest', 'East China', 'South China']
                            ],

                        ),
                        width=3
                    ),
                    # dbc.Col('Platform', width=3),
                    dbc.Col(
                        dcc.Dropdown(
                            id='moving-Platform-Dim-dropdown',
                            placeholder='Platform',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['Baidu', 'ZGC', '2345']
                            ],

                        ),
                        width=3
                    ),
                    # dbc.Col('Software', width=3)
                    dbc.Col(
                        dcc.Dropdown(
                            id='moving-Software-Dim-dropdown',
                            placeholder='Software',
                            options=[
                                {'label': item, 'value': item}
                                for item in ['Kingsoft Antivirus', 'Tencent Manage', '360 Manage', 'Baidu Manage',
                                             '2345HaoZip', 'WinRAR', '360Zip', 'Bandizip', 'QQ Browser', '360 Browser',
                                             'Firefox', 'Chrome']
                            ],

                        ),
                        width=3
                    ),
                ]
            ),
            html.Br(),
            dbc.Row([dbc.Col(dbc.Button('查询', id='moving-query-button'), width=3),
                     # dbc.Col(dbc.Button('连接', id='moving-connect-button'), width=3),
                     # dbc.Col(dbc.Button('测试', id='moving-test-button'), width=3),
                     dcc.Store(id='moving-query-store-1', storage_type='memory'),
                     dcc.Store(id='moving-query-store-2', storage_type='memory'),
                     dcc.Store(id='moving-display-flag-store', storage_type='session')]),
            dbc.Row(html.Pre(id='moving-dropdown-output-1',
                    style={'background-color': '#d4d4d420'})),
            dbc.Row(html.Pre(id='moving-connect-output-1',
                    style={'background-color': '#d4d4d420'})),
            dbc.Row(html.Pre(id='moving-test-output-1',
                    style={'background-color': '#d4d4d420'}))
        ]),
        html.Hr(),
        dbc.Container([], id='moving-figure-container'),
        dcc.Graph(figure=fig, id='scatter'),
        html.Hr(),

    ]
)
