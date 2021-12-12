import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import feffery_antd_components as fac
from dash.dependencies import State

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        fac.AntdRow(
            [
                fac.AntdCol(
                    fac.AntdDatePicker(
                        id='getting-started-date-picker-demo',
                        placeholder='选择日期'
                    )
                ),
                fac.AntdCol(
                    fac.AntdSelect(
                        id='getting-started-select-demo',
                        placeholder='选择你所熟悉的编程语言',
                        options=[
                            {
                                'label': 'Python',
                                'value': 'Python'
                            },
                            {
                                'label': 'R',
                                'value': 'R'
                            },
                            {
                                'label': 'Julia',
                                'value': 'Julia'
                            },
                            {
                                'label': 'JavaScript',
                                'value': 'JavaScript'
                            },
                            {
                                'label': 'Java',
                                'value': 'Java'
                            },
                            {
                                'label': 'Scala',
                                'value': 'Scala'
                            }
                        ],
                        maxTagCount=2,
                        mode='multiple',
                        style={
                            'width': '17rem'
                        }
                    )
                ),
                fac.AntdCol(
                    fac.AntdButton(
                        '提交内容',
                        id='getting-started-button-demo',
                        type='primary'
                    )
                ),
            ],
            gutter=15,
            justify='center'
        ),

        html.Div(id='getting-started-notification-demo')
    ],
    style={
        'height': '500px',
        'display': 'flex',
        'alignItems': 'center',
        'justifyContent': 'center',
        'backgroundColor': 'rgba(241, 241, 241, 0.4)'
    }
)


@app.callback(
    Output('getting-started-notification-demo', 'children'),
    Input('getting-started-button-demo', 'nClicks'),
    [State('getting-started-date-picker-demo', 'selectedDate'),
     State('getting-started-select-demo', 'value')],
    prevent_initial_call=True
)
def getting_started_callback_demo(nClicks, selectedDate, select_value):
    # 若按钮被点击
    if nClicks:
        # 若两个输入组件均有值输入
        if selectedDate and select_value:
            return fac.AntdNotification(
                message='提交成功',
                description='已提交日期：{}，已提交选项值：{}'.format(
                    selectedDate,
                    '、'.join(select_value)
                ),
                type='success',
                duration=3
            )

        return fac.AntdNotification(
            message='提交失败',
            description='信息提交不完整！',
            type='error',
            duration=3
        )


if __name__ == '__main__':
    app.run_server(debug=True)
