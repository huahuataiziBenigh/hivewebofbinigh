from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import dash
from server import app


province2city_dict = {
    '四川省': '成都市',
    '陕西省': '西安市',
    '广东省': '广州市'
}


@app.callback(
    Output('dropdown-output-1', 'children'),
    Input('dropdown-input-1', 'value')
)
def dropdown_output_1(value):
    if value:
        return json.dumps(value, indent=4)

#    return dash.no_update


@app.callback(
    Output('dropdown-output-2', 'children'),
    Input('dropdown-input-2', 'value')
)
def dropdown_output_2(value):
    if value:
        return json.dumps(value, indent=4)

#    return dash.no_update


@app.callback(Output('city', 'children'),
              Input('province', 'value'))
def province2city(province):
    return province2city_dict[province]

