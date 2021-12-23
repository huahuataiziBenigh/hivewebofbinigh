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


@app.callback([# Output('dice-dropdown-output-1', 'children'),
               Output('dice-scatter', 'figure'),
               Output('dice-query-store-1', 'data'),
               Output('dice-display-flag-store', 'data')],
              Input('dice-query-button', 'n_clicks'),
              [State('dice-Time-Dim-dropdown', 'value'),
               State('dice-Area-Dim-dropdown', 'value'),
               State('dice-Platform-Dim-dropdown', 'value'),
               State('dice-Software-Dim-dropdown', 'value')])
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
            dice_dropdown_input = [time_dim, area_dim, platform_dim, software_dim]
            dice_dim_name = ['Month', 'Area_name', 'Platform_name', 'Software_name']
            dice_dim = []
            select_dim = []
            dice_cnt = 0
            for i in range(len(dice_dropdown_input)):
                for item in dice_dropdown_input[i]:
                    if item == 'dice':
                        dice_dim.append(dice_dim_name[i])
                        dice_cnt = dice_cnt + 1
                        break
                    elif item == '*':
                        break
                    elif item != '*':
                        select_dim.append(dice_dim_name[i])
            list(set(select_dim))
            if dice_cnt == 1:
                hql_word = 'Select Month, Area_name, Software_name, Platform_name, sum(Amount_of_Download) as AoD ' \
                           'from TimeDim, DownloadFact, AreaDim, SoftwareDim, PlatformDim ' \
                           'Where DownloadFact.Time_key = TimeDim.Time_key ' \
                           'and DownloadFact.Area_key = AreaDim.Area_key ' \
                           'and DownloadFact.Platform_key = PlatformDim.Platform_key ' \
                           'and DownloadFact.Software_key = SoftwareDim.Software_key '
                for i in range(len(dice_dropdown_input)):
                    hql_word_tmp = 'and ( '
                    for item in dice_dropdown_input[i]:

                        if item == 'dice':
                            break
                        elif item == '*':
                            break
                        else:
                            hql_word_tmp = hql_word_tmp + '{} = '.format(dice_dim_name[i])
                            if type(item) != int:
                                hql_word_tmp = hql_word_tmp + '\'{}\' '.format(item)
                            else:
                                hql_word_tmp = hql_word_tmp + '{} '.format(item)
                            if item == dice_dropdown_input[i][-1]:
                                hql_word_tmp = hql_word_tmp + ') '
                            else:
                                hql_word_tmp = hql_word_tmp + 'or '
                    if hql_word_tmp != 'and ( ':
                        hql_word = hql_word + hql_word_tmp
                hql_word = hql_word + 'Group by Month, Area_name, Software_name, Platform_name '
                print('executing' + hql_word)
                cursor.execute(hql_word)
                print('execute ' + hql_word + ' success')
                query_result = cursor.fetchall()
                query_result = [x.__str__().replace('(', '').replace(')', '').split(', ')
                                for x in query_result]
                print(query_result)
                query_data = DataFrame(query_result,
                                       columns=['Month', 'Area_name', 'Platform_name', 'Software_name', 'AoD'])
                query_data.to_csv('dice_query.csv')
                dice_fig_bar = px.bar(query_data, x=dice_dim[0], y='AoD', color=select_dim[0],
                                      height=600, barmode='group')
                data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
                return dice_fig_bar, data_store, 0

        else:
            '''
            s = [['8', '521289272'], ['9', '605455252'], ['10', '208695106']]
            s = DataFrame(s, columns=['Month', 'AoD'])
            dice_fig_bar = px.bar(s, x="Month", y='AoD', height=500)
            return test_word, dice_fig_bar
            '''
        return fig_test, dash.no_update, dash.no_update
    return dash.no_update, dash.no_update, dash.no_update


@app.callback([Output('dice-Time-Dim-dropdown', 'options'),
               Output('dice-Area-Dim-dropdown', 'options'),
               Output('dice-Platform-Dim-dropdown', 'options'),
               Output('dice-Software-Dim-dropdown', 'options')],
              Input('dice-first-interval', 'n_intervals'))
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
        list1 = ['dice', '*']
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
