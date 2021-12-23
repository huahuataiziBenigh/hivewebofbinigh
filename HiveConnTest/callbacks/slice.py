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


@app.callback([Output('slice-dropdown-output-1', 'children'),
               Output('slice-scatter', 'figure'),
               Output('slice-query-store-1', 'data'),
               Output('slice-display-flag-store', 'data')],
              Input('slice-query-button', 'n_clicks'),
              [State('slice-Time-Dim-dropdown', 'value'),
               State('slice-Area-Dim-dropdown', 'value'),
               State('slice-Platform-Dim-dropdown', 'value'),
               State('slice-Software-Dim-dropdown', 'value')])
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
            slice_dim_cnt = 0
            dim_list = [time_dim, area_dim, platform_dim, software_dim]
            dim_name_list = ['Month', 'Area_name', 'Platform_name', 'Software_name']
            slice_dim = []
            for i in dim_list:
                if i == 'slice':
                    slice_dim_cnt = slice_dim_cnt + 1
            if slice_dim_cnt == 1 or slice_dim_cnt == 2:
                hql_word = 'Select Month, Area_name, Software_name, Platform_name, sum(Amount_of_Download) as AoD ' \
                           'from TimeDim, DownloadFact, AreaDim, SoftwareDim, PlatformDim ' \
                           'Where DownloadFact.Time_key = TimeDim.Time_key ' \
                           'and DownloadFact.Area_key = AreaDim.Area_key ' \
                           'and DownloadFact.Platform_key = PlatformDim.Platform_key ' \
                           'and DownloadFact.Software_key = SoftwareDim.Software_key '
                for i in range(len(dim_list)):
                    if dim_list[i] != 'slice' and dim_list[i] != '*':
                        hql_word = hql_word + 'and {} = '.format(dim_name_list[i])
                        if type(dim_list[i]) != int:
                            hql_word = hql_word + '\'{}\' '.format(dim_list[i])
                        else:
                            hql_word = hql_word + '{} '.format(dim_list[i])
                    elif dim_list[i] == 'slice':
                        slice_dim.append(dim_name_list[i])
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
                query_data.to_csv('slice_query.csv', index=False)
                if slice_dim_cnt == 1:
                    slice_fig_bar = px.bar(query_data, x=slice_dim[0], y='AoD', height=600)
                else:
                    slice_fig_bar = px.density_heatmap(query_data, x=slice_dim[0], y=slice_dim[1], z='AoD',
                                                       height=600, histfunc='sum')
                data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
                return test_word, slice_fig_bar, data_store, 0

            cursor.close()
            conn.close()
        else:
            '''
            s = [['8', '521289272'], ['9', '605455252'], ['10', '208695106']]
            s = DataFrame(s, columns=['Month', 'AoD'])
            slice_fig_bar = px.bar(s, x="Month", y='AoD', height=500)
            return test_word, slice_fig_bar
            '''
        return test_word, fig_test, dash.no_update, dash.no_update, 1
    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, 1


@app.callback([Output('slice-Time-Dim-dropdown', 'options'),
               Output('slice-Area-Dim-dropdown', 'options'),
               Output('slice-Platform-Dim-dropdown', 'options'),
               Output('slice-Software-Dim-dropdown', 'options')],
              Input('slice-first-interval', 'n_intervals'))
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
        list1 = ['slice', '*']
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
