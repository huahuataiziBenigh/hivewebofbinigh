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
               Output('rank-display-flag-store', 'data')],
              Input('scatter', 'clickData'),
              [State('rank-query-store-1', 'data'),
               State('rank-display-flag-store', 'data')])
def listen_to_figure(click_data, store_data, flag_data):
    if store_data:
        df_data = pd.read_csv('rank_query.csv')
        if not df_data.empty:
            if flag_data == 0:
                if store_data['time'] == 'rank':
                    mask_time = df_data['Month'] == click_data['points'][0]['x']
                    query_data = df_data[mask_time]
                    rank_fig_bar = px.line(query_data, x="Day", y='AoD', height=600)
                    return rank_fig_bar, 1
                elif store_data['area'] == 'rank':
                    mask_area = df_data['Area'] == click_data['points'][0]['x']
                    query_data = df_data[mask_area]
                    rank_fig_bar = px.line(query_data, x="Province", y='AoD', height=600)
                    return rank_fig_bar, 1
            elif flag_data == 1:
                if store_data['time'] == 'rank':
                    # query_data = df_data['AoD'].groupby(df_data['Month']).sum().reset_index()
                    rank_fig_bar = px.bar(df_data, x="Month", y='AoD', height=600)
                    return rank_fig_bar, 0
                elif store_data['area'] == 'rank':
                    # query_data = df_data['AoD'].groupby(df_data['Area']).sum().reset_index()
                    rank_fig_bar = px.bar(df_data, x="Area", y='AoD', height=600)
                    return rank_fig_bar, 0
    return dash.no_update
'''


@app.callback([
    Output('rank-scatter', 'figure'),
    Output('rank-query-store-1', 'data'),
    Output('rank-display-flag-store', 'data')],
    Input('rank-query-button', 'n_clicks'),
    [State('rank-Time-Dim-dropdown', 'value'),
     State('rank-Area-Dim-dropdown', 'value'),
     State('rank-Platform-Dim-dropdown', 'value'),
     State('rank-Software-Dim-dropdown', 'value')])
def test_callback(n_clicks, time_dim, area_dim, platform_dim, software_dim):
    if n_clicks:
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
            rank_dim_cnt = 0
            dim_list = [time_dim, area_dim, platform_dim, software_dim]
            dim_name_list = ['Month', 'Area_name', 'Platform_name', 'Software_name']
            rank_dim = []
            for i in dim_list:
                if i == 'rank':
                    rank_dim_cnt = rank_dim_cnt + 1

            if rank_dim_cnt == 1 or rank_dim_cnt == 2:

                hql_word = 'Select Month, Area_name, Software_name, Platform_name, sum(Amount_of_Download) as AoD ' \
                           'from TimeDim, DownloadFact, AreaDim, SoftwareDim, PlatformDim ' \
                           'Where DownloadFact.Time_key = TimeDim.Time_key ' \
                           'and DownloadFact.Area_key = AreaDim.Area_key ' \
                           'and DownloadFact.Platform_key = PlatformDim.Platform_key ' \
                           'and DownloadFact.Software_key = SoftwareDim.Software_key '
                for i in range(len(dim_list)):
                    if dim_list[i] != 'rank' and dim_list[i] != '*':
                        hql_word = hql_word + 'and {} = '.format(dim_name_list[i])
                        if type(dim_list[i]) != int:
                            hql_word = hql_word + '\'{}\' '.format(dim_list[i])
                        else:
                            hql_word = hql_word + '{} '.format(dim_list[i])
                    elif dim_list[i] == 'rank':
                        rank_dim.append(dim_name_list[i])
                hql_word = hql_word + 'Group by Month, Area_name, Software_name, Platform_name '
                print('executing')
                cursor.execute(hql_word)
                print('execute ' + hql_word + ' success')
                query_result = cursor.fetchall()
                query_result = [x.__str__().replace('(', '').replace(')', '').split(', ')
                                for x in query_result]
                # print(query_result)
                query_data = DataFrame(query_result,
                                       columns=['Month', 'Area_name', 'Platform_name', 'Software_name', 'AoD'])
                query_data.to_csv('rank_query.csv', index=False)

                query_data = pd.read_csv('rank_query.csv')
                if not rank_dim:
                    rank_dim = ['Area_name', 'Month']
                rank_fig_output = go.Figure()
                if rank_dim_cnt == 1:
                    query_data1 = query_data['AoD'].groupby(query_data[rank_dim[0]]).sum().reset_index()
                    rank_fig_output.add_trace(go.Bar(x=query_data1[rank_dim[0]], y=query_data1['AoD']))
                    # rank_fig_bar = px.bar(query_data, x=rank_dim[0], y='AoD', height=600)
                else:
                    for rank_1, query_data1 in query_data.groupby(rank_dim[1]):
                        rank_fig_output.add_trace(go.Bar(x=query_data1[rank_dim[0]], y=query_data1['AoD'], name=rank_1))

                    # rank_fig_bar = px.bar(query_data, x=rank_dim[0], color=rank_dim[1], y='AoD',
                    #                       height=600, barmode='group')
                gb_list = []
                for i in rank_dim:
                    gb_list.append(query_data[i])
                q_max = query_data['AoD'].groupby(gb_list).sum().max()
                q_min = query_data['AoD'].groupby(gb_list).sum().min()
                threshold_base = q_max - q_min
                # print(threshold_base)
                threshold_tmp = q_min
                # print(threshold_tmp)
                threshold_list = [threshold_tmp + threshold_base / 4 * i for i in range(1, 4)]
                # print(threshold_list)
                # threshold_dict = {'threshold': threshold_list}
                # threshold_df = pd.DataFrame(threshold_dict)
                threshold_df = query_data.assign(key=1).merge(pd.DataFrame({'key': [1] * len(threshold_list),
                                                                            'id': ['Lv3', 'Lv2', 'Lv1'],
                                                                            'v': threshold_list})).drop('key', 1)
                # print(threshold_df)
                for rank_2, threshold_data2 in threshold_df.groupby('id'):
                    rank_fig_output.add_trace(go.Scatter(x=threshold_data2[rank_dim[0]], y=threshold_data2['v'],
                                                         name=rank_2, mode='lines+markers'))
                rank_fig_output.update_layout(height=600)
                # rank_fig_line = px.line(threshold_df, color='id', x=rank_dim[0], y='v', height=600)
                # rank_fig_output = go.Figure()
                # rank_fig_output.add_trace(rank_fig_bar)  # .add_trace(rank_fig_line)
                data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
                return rank_fig_output, data_store, 0

            # return test_word, fig_test, dash.no_update, dash.no_update
            cursor.close()
            conn.close()
        else:
            '''
            s = [['8', '521289272'], ['9', '605455252'], ['10', '208695106']]
            s = DataFrame(s, columns=['Month', 'AoD'])
            rank_fig_bar = px.bar(s, x="Month", y='AoD', height=500)
            return test_word, rank_fig_bar
            '''
        return fig_test, dash.no_update, dash.no_update
    return dash.no_update, dash.no_update, dash.no_update


'''
@app.callback(Output('rank-connect-output-1', 'children'),
              Input('rank-connect-button', 'n_clicks'),
              prevent_initial_call=True)
def connect_test(n_clicks):
    if n_clicks:
        conn = connect_hive()
        cur = conn.cursor()
        cur.close()
        conn.close()
        return 'connect success'
    return dash.no_update


@app.callback([Output('rank-dropdown-output-1', 'children'),
               Output('scatter', 'figure'),
               Output('rank-query-store-1', 'data'),
               Output('rank-query-store-2', 'data'),
               Output('rank-display-flag-store', 'data')],
              Input('rank-test-button', 'n_clicks'))
def rank_func_test(n_clicks):
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



@app.callback([Output('rank-dropdown-output-1', 'children'),
               Output('scatter', 'figure'),
               Output('rank-query-store-1', 'data')],
              Input('rank-test-button', 'n_clicks'),
              State('rank-query-store-1', 'data'))
def rank_func_test(n_clicks, st_data):
    if n_clicks:
        time_dim = 'rank'
        area_dim = '*'
        platform_dim = '*'
        software_dim = '*'
        fig_test = px.scatter(x=range(n_clicks), y=range(n_clicks), height=400)
        fig_test.update_layout(clickmode='event+select')  # 设置点击模式
        test_word = 'n:{}, t:{}, a：{}, p:{}, s:{}'.format(n_clicks, time_dim, area_dim, platform_dim, software_dim)
        # print(test_word)
        data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
        # print(data_store)
        query_data = pd.read_csv('rank_query.csv')

        # print(query_data)
        rank_fig_bar = px.bar(query_data, x="Month", y='AoD', height=600)

        return test_word, rank_fig_bar, data_store
    return dash.no_update
'''


@app.callback([Output('rank-Time-Dim-dropdown', 'options'),
               Output('rank-Area-Dim-dropdown', 'options'),
               Output('rank-Platform-Dim-dropdown', 'options'),
               Output('rank-Software-Dim-dropdown', 'options')],
              Input('rank-first-interval', 'n_intervals'))
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
        list1 = ['rank', '*']
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
    Output('rank-dropdown-container', 'children'),
    Input('rank-select-TorA-dropdown', 'value'),
    State('rank-select-TorA-dropdown', 'children'),
    prevent_initial_call=True
)
def dropdown_output_1(value, children):
    if value == 'Time':
        children.append(
            dbc.Row(
                [
                    dcc.Dropdown(
                        id='rank-select-area-dropdown',
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
