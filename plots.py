import plotly.graph_objects as go
import json
import plotly


def get_temperature_plot(df):
    fig = go.Figure(
        layout={
            'title': {
                'text': 'Температура',
                'xanchor': 'left',
                'xref': 'paper',
                'x': 0,
                'y': 0.92
            },
            'yaxis_title': "°C",
            'yaxis_side': 'right',
            'margin': {
                't': 40,
                'b': 10
            }
        }
    )

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['thermometer_top'],
        line_color='rgb(238,130,238)',
        name='Верхний',
    ))

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['thermometer_bottom'],
        line_color='rgb(106,90,205)',
        name='Нижний',
    ))

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['thermometer_external'],
        line_color='rgb(0,100,0)',
        name='Внешний',
    ))

    fig.add_trace(go.Scatter(
        x=df['ts'], y=[30] * df.shape[0],
        line_color='rgb(255,210,210)',
        name='Плохо',
    ))

    fig.update_traces(mode='lines')
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_co2_plot(df):
    fig = go.Figure(
        layout={
            'title': {
                'text': 'CO2',
                'xanchor': 'left',
                'xref': 'paper',
                'x': 0,
                'y': 0.92
            },
            'yaxis_title': "PPM",
            'yaxis_side': 'right',
            'margin': {
                't': 40,
                'b': 10
            }
        }
    )

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['co2'],
        line_color='rgb(124,185,232)',
        name='CO2',
    ))

    fig.update_traces(mode='lines')
    fig.update_layout(showlegend=True)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_humidity_plot(df):
    fig = go.Figure(
        layout={
            'title': {
                'text': 'Влажность воздуха',
                'xanchor': 'left',
                'xref': 'paper',
                'x': 0,
                'y': 0.92
            },
            'yaxis_title': "%",
            'yaxis_side': 'right',
            'margin': {
                't': 40,
                'b': 10
            }
        }
    )

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['humidity'],
        line_color='rgb(124,185,232)',
        name='Humidity',
    ))

    fig.update_traces(mode='lines')
    fig.update_layout(showlegend=True)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_soil_moisture_plot(df):
    fig = go.Figure(
        layout={
            'title': {
                'text': 'Влажность почвы',
                'xanchor': 'left',
                'xref': 'paper',
                'x': 0,
                'y': 0.92
            },
            'yaxis_title': "Ед.",
            'yaxis_side': 'right',
            'margin': {
                't': 40,
                'b': 10
            }
        }
    )

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['soil_moisture_top'],
        line_color='rgb(255,166,77)',
        name='Верхняя полка',
    ))

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['soil_moisture_bottom'],
        line_color='rgb(153,77,0)',
        name='Нижняя полка',
    ))

    watering_top = df.groupby('last_watering_time_top').first().reset_index()[1:]
    fig.add_trace(go.Scatter(
        x=watering_top['last_watering_time_top'], y=watering_top['soil_moisture_top'],
        line_color='rgb(255,0,0)',
        mode='markers',
        name='Полив, верх',
    ))

    watering_bottom = df.groupby('last_watering_time_bottom').first().reset_index()[1:]
    fig.add_trace(go.Scatter(
        x=watering_bottom['last_watering_time_bottom'], y=watering_bottom['soil_moisture_bottom'],
        line_color='rgb(255,0,0)',
        mode='markers',
        name='Полив, низ',
    ))

    fig.update_layout(showlegend=True)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)


def get_lighting_plot(df):
    fig = go.Figure(
        layout={
            'title': {
                'text': 'Работа освещения',
                'xanchor': 'left',
                'xref': 'paper',
                'x': 0,
                'y': 0.92
            },
            'yaxis_title': "№ группы ламп",
            'yaxis_side': 'right',
            'margin': {
                't': 40,
                'b': 10
            }
        }
    )
    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['light_1'].apply(lambda x: None if x < 0 else x),
        line_color='rgb(255,0,0)',
        name='Группа 1',
        connectgaps=False
    ))

    fig.add_trace(go.Scatter(
        x=df['ts'], y=df['light_2'].apply(lambda x: None if x < 0 else x),
        line_color='rgb(0,0,255)',
        name='Группа 2',
        connectgaps=False
    ))

    fig.update_traces(mode='lines')
    fig.update_layout(showlegend=True)
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)