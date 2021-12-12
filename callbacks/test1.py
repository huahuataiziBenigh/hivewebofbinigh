from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import dash
from application import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from impala.dbapi import connect
from connect_hive import connect_hive
from pandas import DataFrame

'''
# 多对多的回调函数
@app.callback([Output('hover', 'children'),
               Output('click', 'children'),
               Output('select', 'children'),
               Output('zoom', 'children'), ],
              [Input('scatter', 'hoverData'),
               Input('scatter', 'clickData'),
               Input('scatter', 'selectedData'),
               Input('scatter', 'relayoutData')])
def listen_to_hover(hoverData, clickData, selectedData, relayoutData):
    return str(hoverData), str(clickData), str(selectedData), str(relayoutData)


@app.callback([Output('scatter', 'figure'),
               Output('rollup-display-flag-store', 'data')],
              Input('scatter', 'clickData'),
              [State('rollup-query-store-1', 'data'),
               State('rollup-display-flag-store', 'data')])
def listen_to_figure(click_data, store_data, flag_data):
    if store_data:
        df_data = pd.read_csv('rollup_query.csv')
        if not df_data.empty:
            if flag_data == 0:
                if store_data['time'] == 'rollup':
                    mask_time = df_data['Month'] == click_data['points'][0]['x']
                    query_data = df_data[mask_time]
                    rollup_fig_bar = px.line(query_data, x="Day", y='AoD', height=600)
                    return rollup_fig_bar, 1
                elif store_data['area'] == 'rollup':
                    mask_area = df_data['Area'] == click_data['points'][0]['x']
                    query_data = df_data[mask_area]
                    rollup_fig_bar = px.line(query_data, x="Province", y='AoD', height=600)
                    return rollup_fig_bar, 1
            elif flag_data == 1:
                if store_data['time'] == 'rollup':
                    # query_data = df_data['AoD'].groupby(df_data['Month']).sum().reset_index()
                    rollup_fig_bar = px.bar(df_data, x="Month", y='AoD', height=600)
                    return rollup_fig_bar, 0
                elif store_data['area'] == 'rollup':
                    # query_data = df_data['AoD'].groupby(df_data['Area']).sum().reset_index()
                    rollup_fig_bar = px.bar(df_data, x="Area", y='AoD', height=600)
                    return rollup_fig_bar, 0
    return dash.no_update
'''''''''


@app.callback([Output('scatter', 'figure'),
               Output('rollup-query-store-1', 'data'),
               Output('rollup-display-flag-store', 'data')],
              [Input('rollup-query-button', 'n_clicks'),
               Input('scatter', 'clickData')],
              [State('rollup-Time-Dim-dropdown', 'value'),
               State('rollup-Area-Dim-dropdown', 'value'),
               State('rollup-Platform-Dim-dropdown', 'value'),
               State('rollup-Software-Dim-dropdown', 'value'),
               State('rollup-query-store-1', 'data'),
               State('rollup-display-flag-store', 'data')])
def test_callback(n_clicks, click_data, time_dim, area_dim, platform_dim, software_dim, store_data, flag_data):
    ctx = dash.callback_context
    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'rollup-query-button':
        fig_test = px.scatter(x=range(n_clicks), y=range(n_clicks), height=600)
        fig_test.update_layout(clickmode='event+select')  # 设置点击模式
        test_word = 'n:{}, t:{}, a：{}, p:{}, s:{}'.format(n_clicks, time_dim, area_dim,
                                                          platform_dim, software_dim)
        if time_dim and area_dim and platform_dim and software_dim:
            conn = connect_hive()
            cursor = conn.cursor()
            hql_word = 'use sw'
            cursor.execute(hql_word)
            print('use sw success')
            if time_dim == 'rollup' and area_dim != 'rollup' and platform_dim != 'rollup' and software_dim != 'rollup':
                hql_word = 'Select Month, Day, sum(Amount_of_Download) as AoD ' \
                           'from TimeDim, DownloadFact, AreaDim, SoftwareDim, PlatformDim ' \
                           'Where DownloadFact.Time_key = TimeDim.Time_key ' \
                           'and DownloadFact.Area_key = AreaDim.Area_key ' \
                           'and DownloadFact.Platform_key = PlatformDim.Platform_key ' \
                           'and DownloadFact.Software_key = SoftwareDim.Software_key '
                if area_dim != '*':
                    hql_word = hql_word + 'and Area_name = \"{}\" '.format(area_dim)
                if platform_dim != '*':
                    hql_word = hql_word + 'and Platform_name = \"{}\" '.format(platform_dim)
                if software_dim != '*':
                    hql_word = hql_word + 'and Software_name = \"{}\" '.format(software_dim)
                hql_word = hql_word + 'Group by Month, Day'
                print('executing')
                cursor.execute(hql_word)
                print('execute ' + hql_word + ' success')
                query_result = cursor.fetchall()
                query_result = [x.__str__().replace('(', '').replace(')', '').split(', ')
                                for x in query_result]
                print(query_result)
                query_data = DataFrame(query_result, columns=['Month', 'Day', 'AoD'])
                query_data.to_csv('rollup_query.csv', index=False)
                rollup_fig_bar = px.bar(query_data, x="Month", y='AoD', height=600)
                data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
                return test_word, rollup_fig_bar, data_store, 0
            elif time_dim != 'rollup' and area_dim == 'rollup' and platform_dim != 'rollup' and software_dim != 'rollup':
                hql_word = 'Select Area_name, Province_name, sum(Amount_of_Download) as AoD ' \
                           'from TimeDim, DownloadFact, AreaDim, SoftwareDim, PlatformDim ' \
                           'Where DownloadFact.Time_key = TimeDim.Time_key ' \
                           'and DownloadFact.Area_key = AreaDim.Area_key ' \
                           'and DownloadFact.Platform_key = PlatformDim.Platform_key ' \
                           'and DownloadFact.Software_key = SoftwareDim.Software_key '
                if time_dim != '*':
                    hql_word = hql_word + 'and Month = {} '.format(time_dim)
                if platform_dim != '*':
                    hql_word = hql_word + 'and Platform_name = \"{}\" '.format(platform_dim)
                if software_dim != '*':
                    hql_word = hql_word + 'and Software_name = \"{}\" '.format(software_dim)
                hql_word = hql_word + 'Group by Area_name, Province_name'
                print('executing')
                cursor.execute(hql_word)
                print('execute ' + hql_word + ' success')
                query_result = cursor.fetchall()
                query_result = [x.__str__().replace('(', '').replace(')', '').split(', ')
                                for x in query_result]
                print(query_result)
                query_data = DataFrame(query_result, columns=['Area', 'Province', 'AoD'])
                query_data.to_csv('rollup_query.csv', index=False)
                rollup_fig_bar = px.bar(query_data, x="Area", y='AoD', height=600)
                data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
                return rollup_fig_bar, data_store, 0
            cursor.close()
            conn.close()
        else:
            '''
            s = [['8', '521289272'], ['9', '605455252'], ['10', '208695106']]
            s = DataFrame(s, columns=['Month', 'AoD'])
            rollup_fig_bar = px.bar(s, x="Month", y='AoD', height=500)
            return test_word, rollup_fig_bar
            '''
        return fig_test, dash.no_update, dash.no_update
    else:
        if store_data:
            df_data = pd.read_csv('rollup_query.csv')
            if not df_data.empty:
                if flag_data == 0:
                    if store_data['time'] == 'rollup':
                        mask_time = df_data['Month'] == click_data['points'][0]['x']
                        query_data = df_data[mask_time]
                        rollup_fig_bar = px.line(query_data, x="Day", y='AoD', height=600)
                        return rollup_fig_bar, 1
                    elif store_data['area'] == 'rollup':
                        mask_area = df_data['Area'] == click_data['points'][0]['x']
                        query_data = df_data[mask_area]
                        rollup_fig_bar = px.line(query_data, x="Province", y='AoD', height=600)
                        return rollup_fig_bar, 1
                elif flag_data == 1:
                    if store_data['time'] == 'rollup':
                        # query_data = df_data['AoD'].groupby(df_data['Month']).sum().reset_index()
                        rollup_fig_bar = px.bar(df_data, x="Month", y='AoD', height=600)
                        return rollup_fig_bar, 0
                    elif store_data['area'] == 'rollup':
                        # query_data = df_data['AoD'].groupby(df_data['Area']).sum().reset_index()
                        rollup_fig_bar = px.bar(df_data, x="Area", y='AoD', height=600)
                        return rollup_fig_bar, 0
    return dash.no_update, dash.no_update, dash.no_update


@app.callback(Output('rollup-connect-output-1', 'children'),
              Input('rollup-connect-button', 'n_clicks'),
              prevent_initial_call=True)
def connect_test(n_clicks):
    if n_clicks:
        conn = connect_hive()
        cur = conn.cursor()
        cur.close()
        conn.close()
        return 'connect success'
    return dash.no_update


'''
@app.callback([Output('rollup-dropdown-output-1', 'children'),
               Output('scatter', 'figure'),
               Output('rollup-query-store-1', 'data'),
               Output('rollup-query-store-2', 'data'),
               Output('rollup-display-flag-store', 'data')],
              Input('rollup-test-button', 'n_clicks'))
def rollup_func_test(n_clicks):
    if n_clicks:
        time_dim = '11'
        area_dim = '22'
        platform_dim = '33'
        software_dim = '44'
        fig_test = px.scatter(x=range(n_clicks), y=range(n_clicks), height=400)
        fig_test.update_layout(clickmode='event+select')  # 设置点击模式
        test_word = 'n:{}, t:{}, a：{}, p:{}, s:{}'.format(n_clicks, time_dim, area_dim, platform_dim, software_dim)
        print(test_word)
        data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
        print(data_store)
        query_data = pd.read_csv('test_data.csv')
        print(query_data)
        return test_word, fig_test, data_store, query_data, 0
    return dash.no_update
'''


@app.callback([Output('rollup-dropdown-output-1', 'children'),
               Output('scatter', 'figure'),
               Output('rollup-query-store-1', 'data')],
              Input('rollup-test-button', 'n_clicks'),
              State('rollup-query-store-1', 'data'))
def rollup_func_test(n_clicks, st_data):
    if n_clicks:
        time_dim = 'rollup'
        area_dim = '*'
        platform_dim = '*'
        software_dim = '*'
        fig_test = px.scatter(x=range(n_clicks), y=range(n_clicks), height=400)
        fig_test.update_layout(clickmode='event+select')  # 设置点击模式
        test_word = 'n:{}, t:{}, a：{}, p:{}, s:{}'.format(n_clicks, time_dim, area_dim, platform_dim, software_dim)
        # print(test_word)
        data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
        # print(data_store)
        query_data = pd.read_csv('rollup_query.csv')

        # print(query_data)
        rollup_fig_bar = px.bar(query_data, x="Month", y='AoD', height=600)

        return test_word, rollup_fig_bar, data_store
    return dash.no_update


@app.callback([Output('rollup-Time-Dim-dropdown', 'options'),
               Output('rollup-Area-Dim-dropdown', 'options'),
               Output('rollup-Platform-Dim-dropdown', 'options'),
               Output('rollup-Software-Dim-dropdown', 'options')],
              Input('rollup-first-interval', 'n_intervals'))
def initial_dim(n_intervals):
    if n_intervals:
        conn = connect_hive()
        cur = conn.cursor()
        hql_word = 'use sw'
        cur.execute(hql_word)
        print('use sw success')
        hql_word = 'Select Month from TimeDim'
        cur.execute(hql_word)
        print('execute ' + hql_word + ' success')
        time_dim_month = cur.fetchall()
        time_dim_month = [x.__str__().replace('(', '').replace(')', '').replace(',', '').replace('\'', '')
                          for x in list(set(time_dim_month))]
        list1 = ['rollup', '*']
        options_time = [{'label': item, 'value': item} for item in list1 + time_dim_month]
        hql_word = 'Select Area_name from AreaDim'
        cur.execute(hql_word)
        print('execute ' + hql_word + ' success')
        area_dim_month = cur.fetchall()
        area_dim_month = [x.__str__().replace('(', '').replace(')', '').replace(',', '').replace('\'', '')
                          for x in list(set(area_dim_month))]
        options_area = [{'label': item, 'value': item} for item in list1 + area_dim_month]
        hql_word = 'Select Platform_name from PlatformDim'
        cur.execute(hql_word)
        print('execute ' + hql_word + ' success')
        platform_dim_month = cur.fetchall()
        platform_dim_month = [x.__str__().replace('(', '').replace(')', '').replace(',', '').replace('\'', '')
                              for x in list(set(platform_dim_month))]
        options_platform = [{'label': item, 'value': item} for item in list1 + platform_dim_month]
        hql_word = 'Select Software_name from SoftwareDim'
        cur.execute(hql_word)
        print('execute ' + hql_word + ' success')
        software_dim_month = cur.fetchall()
        software_dim_month = [x.__str__().replace('(', '').replace(')', '').replace(',', '').replace('\'', '')
                              for x in list(set(software_dim_month))]
        options_software = [{'label': item, 'value': item} for item in list1 + software_dim_month]
        return options_time, options_area, options_platform, options_software
    return dash.no_update


'''
@app.callback(
    Output('rollup-dropdown-container', 'children'),
    Input('rollup-select-TorA-dropdown', 'value'),
    State('rollup-select-TorA-dropdown', 'children'),
    prevent_initial_call=True
)
def dropdown_output_1(value, children):
    if value == 'Time':
        children.append(
            dbc.Row(
                [
                    dcc.Dropdown(
                        id='rollup-select-area-dropdown',
                        placeholder='单选',
                        options=[
                            {'label': item, 'value': item}
                            for item in ['Time', 'Area']
                        ],
                        style={
                            'width': '300px'
                        },
                        value='Time'
                    ),
                ]
            )
        )
        return children
'''
