from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import json
import dash
from server import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from impala.dbapi import connect
from connect_hive import connect_hive
from pandas import DataFrame


@app.callback([Output('pivot-scatter', 'figure'),
               Output('pivot-display-flag-store', 'data')],
              Input('pivot-scatter', 'clickData'),
              [State('pivot-query-store-1', 'data'),
               State('pivot-display-flag-store', 'data')])
def listen_to_figure(click_data, store_data, flag_data):
    if store_data:
        df_data = pd.read_csv('pivot_query.csv')
        if not df_data.empty:
            if flag_data == 0:
                pivot_fig_bar = px.bar(df_data, x=store_data['dim2'], color=store_data['dim1'], y='AoD',
                                       height=600, barmode='group')
                pivot_fig_bar.update_layout(barmode='group')
                return pivot_fig_bar, 1
            else:
                pivot_fig_bar = px.bar(df_data, x=store_data['dim1'], color=store_data['dim2'], y='AoD',
                                       height=600, barmode='group')
                pivot_fig_bar.update_layout(barmode='group')
                return pivot_fig_bar, 0
    return dash.no_update


@app.callback([
               Output('pivot-scatter', 'figure'),
               Output('pivot-query-store-1', 'data'),
               Output('pivot-display-flag-store', 'data')],
              Input('pivot-query-button', 'n_clicks'),
              [State('pivot-Time-Dim-dropdown', 'value'),
               State('pivot-Area-Dim-dropdown', 'value'),
               State('pivot-Platform-Dim-dropdown', 'value'),
               State('pivot-Software-Dim-dropdown', 'value')])
def test_callback(n_clicks, time_dim, area_dim, platform_dim, software_dim):
    if n_clicks:
        fig_test = px.scatter(x=range(n_clicks), y=range(n_clicks), height=400)
        fig_test.update_layout(clickmode='event+select')  # 设置点击模式
        test_word = 'n:{}, t:{}, a：{}, p:{}, s:{}'.format(n_clicks, time_dim, area_dim,
                                                          platform_dim, software_dim)
        if time_dim and area_dim and platform_dim and software_dim:
            conn = connect_hive()
            cursor = conn.cursor()
            hql_word = 'use sw'
            cursor.execute(hql_word)
            print('use sw success')
            pivot_dim_cnt = 0
            dim_list = [time_dim, area_dim, platform_dim, software_dim]
            dim_name_list = ['Month', 'Area_name', 'Platform_name', 'Software_name']
            pivot_dim = []
            for i in dim_list:
                if i == 'pivot':
                    pivot_dim_cnt = pivot_dim_cnt + 1
            if pivot_dim_cnt == 2:
                hql_word = 'Select Month, Area_name, Software_name, Platform_name, sum(Amount_of_Download) as AoD ' \
                           'from TimeDim, DownloadFact, AreaDim, SoftwareDim, PlatformDim ' \
                           'Where DownloadFact.Time_key = TimeDim.Time_key ' \
                           'and DownloadFact.Area_key = AreaDim.Area_key ' \
                           'and DownloadFact.Platform_key = PlatformDim.Platform_key ' \
                           'and DownloadFact.Software_key = SoftwareDim.Software_key '
                for i in range(len(dim_list)):
                    if dim_list[i] != 'pivot' and dim_list[i] != '*':
                        hql_word = hql_word + 'and {} = '.format(dim_name_list[i])
                        if type(dim_list[i]) != int:
                            hql_word = hql_word + '\'{}\' '.format(dim_list[i])
                        else:
                            hql_word = hql_word + '{} '.format(dim_list[i])
                    elif dim_list[i] == 'pivot':
                        pivot_dim.append(dim_name_list[i])
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
                query_data.to_csv('pivot_query.csv', index=False)
                pivot_fig_bar = px.bar(query_data, x=pivot_dim[0], color=pivot_dim[1], y='AoD',
                                       height=600, barmode='group')
                data_store = {'dim1': pivot_dim[0], 'dim2': pivot_dim[1]}
                return test_word, pivot_fig_bar, data_store, 0

            cursor.close()
            conn.close()
        else:
            '''
            s = [['8', '521289272'], ['9', '605455252'], ['10', '208695106']]
            s = DataFrame(s, columns=['Month', 'AoD'])
            pivot_fig_bar = px.bar(s, x="Month", y='AoD', height=500)
            return test_word, pivot_fig_bar
            '''
        return fig_test, dash.no_update, dash.no_update, 1
    return dash.no_update, dash.no_update, dash.no_update, 1


@app.callback([Output('pivot-Time-Dim-dropdown', 'options'),
               Output('pivot-Area-Dim-dropdown', 'options'),
               Output('pivot-Platform-Dim-dropdown', 'options'),
               Output('pivot-Software-Dim-dropdown', 'options')],
              Input('pivot-first-interval', 'n_intervals'))
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
        list1 = ['pivot', '*']
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
