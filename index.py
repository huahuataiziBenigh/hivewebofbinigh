# import dash_html_components as html
# import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import dash
from dash import html, dcc
# from views.index import index_page
# from views.age import age_page
# from views.sex import sex_page
# from views.statistics import statistics_page
from views.test1 import test1_page
from views.slice import slice_page
from views.dice import dice_page
from views.moving import moving_page
from views.rank import rank_page
from views.pivot import pivot_page
from views.cross import cross_page

from application import app

server = app.server
app.layout = html.Div([
        # 监听url变化
        dcc.Location(id='url'),
        html.Div(
            [
                # 标题区域
                html.Div(

                    html.H3(
                        'Hive OLAP',
                        style={
                            'marginTop': '20px',
                            'fontFamily': 'SimSun',
                            'fontWeight': 'bold'
                        }
                    ),
                    style={
                        'textAlign': 'center',
                        'margin': '0 10px 0 10px',
                        'borderBottom': '2px solid black'
                    }
                ),

                # 子页面区域
                html.Hr(),

                dbc.Nav(
                    [
                        dbc.NavLink('drill & roll', href='/', active="exact", external_link=True),
                        dbc.NavLink('slice', href='/slice', active="exact", external_link=True),
                        dbc.NavLink('dice', href='/dice', active="exact", external_link=True),
                        dbc.NavLink('movingAvg&Sum', href='/moving', active="exact", external_link=True),
                        dbc.NavLink('rank', href='/rank', active="exact", external_link=True),
                        dbc.NavLink('pivot', href='/pivot', active="exact", external_link=True),
                        dbc.NavLink('cross tab', href='/cross', active="exact", external_link=True),
                    ],
                    vertical=True,
                    pills=True
                )
            ],
            style={
                'flex': 'none',
                'width': '300px',
                'backgroundColor': '#fafafa'
            }
        ),
        html.Div(
            id='page-content',
            style={
                'flex': 'auto'
            }
        )
    ],
    style={
        'width': '100vw',
        'height': '100vh',
        'display': 'flex'
    })


# 路由总控
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def render_page_content(pathname):
    if pathname == '/':
        return test1_page
#        return index_page

    elif pathname == '/slice':
        return slice_page
#        return age_page

    elif pathname == '/dice':
        return dice_page
#        return sex_page

    elif pathname == '/moving':
        return moving_page
#        return statistics_page

    elif pathname == '/rank':
        return rank_page
#        return statistics_page

    elif pathname == '/pivot':
        return pivot_page
#        return statistics_page

    elif pathname == '/cross':
        return cross_page
#        return statistics_page

    elif pathname == '/test1':
        return test1_page

    return html.H1('您访问的页面不存在！')


if __name__ == '__main__':
    app.run_server(debug=True)

