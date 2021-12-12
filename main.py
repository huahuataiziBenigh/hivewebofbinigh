# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

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


if __name__ == '__main__':
    time_dim = 'slice'
    area_dim = 'slice'
    platform_dim = '*'
    software_dim = '360Zip'
    '''
    conn = connect_hive()
    cursor = conn.cursor()
    hql_word = 'use sw'
    cursor.execute(hql_word)
    print('use sw success')
    '''

    slice_dim_cnt = 0
    dim_list = [time_dim, area_dim, platform_dim, software_dim]
    dim_name_list = ['Month', 'Area_name', 'Platform_name', 'Software_name']
    slice_dim = []
    for i in dim_list:
        if i == 'slice':
            slice_dim_cnt = slice_dim_cnt + 1
    print(slice_dim_cnt)
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
    print(slice_dim)
    hql_word = hql_word + 'Group by Month, Area_name, Software_name, Platform_name '
    print('executing ' + hql_word)
    '''
    cursor.execute(hql_word)
    print('execute ' + hql_word + ' success')
    query_result = cursor.fetchall()
    query_result = [x.__str__().replace('(', '').replace(')', '').split(', ')
                    for x in query_result]
    print(query_result)
    query_data = DataFrame(query_result,
                           columns=['Month', 'Area_name', 'Platform_name', 'Software_name', 'AoD'])
    query_data.to_csv('test_data.csv', index=False)
    '''
    query_data = pd.read_csv('test_data.csv')
    # print(query_data)
    '''
    df = px.data.tips()
    print(df)
    fig = px.density_heatmap(df, x="total_bill", y="tip", marginal_x="histogram", marginal_y="histogram")
    fig.show()
    '''

    if slice_dim_cnt:
        slice_fig_bar = px.bar(query_data, x=slice_dim[0], y='AoD', height=800)
    else:
        slice_fig_bar = px.density_heatmap(query_data, x=slice_dim[0], y=slice_dim[1], z='AoD',
                                           height=800, histfunc='sum')
    slice_fig_bar.show()
    #print(slice_fig_bar)

    data_store = {'time': time_dim, 'area': area_dim, 'platform': platform_dim, 'software': software_dim}
    print(data_store)
    print(type(data_store))


