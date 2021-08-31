import mysql.connector
import pandas as pd
import json

from config.db import USER, PASSWORD, HOST, PORT, DATABASE

WINDOW_SHORT = 60
WINDOW_LONG = 600


def get_log(date_from, date_to):
    with mysql.connector.connect(user=USER, password=PASSWORD, host=HOST, port=PORT, database=DATABASE) as cnx:
        log = pd.read_sql(
            'SELECT id, ts, log FROM log WHERE ts BETWEEN %s AND %s',
            params=(date_from, date_to),
            con=cnx,
            index_col='id'
        )
        log['log'] = log['log'].apply(json.loads)
        log['thermometer_top'] = log['log'].apply(lambda x: x['thermometer']['top'])
        log['thermometer_bottom'] = log['log'].apply(lambda x: x['thermometer']['bottom'])
        log['thermometer_external'] = log['log'].apply(lambda x: x['thermometer']['external'])
        log['co2'] = log['log'].apply(lambda x: x['co2']['co2'])
        log['humidity'] = log['log'].apply(lambda x: x['humidity']['humidity'])
        log['soil_moisture_top'] = log['log'].apply(lambda x: x['soil_moisture']['top'])
        log['soil_moisture_bottom'] = log['log'].apply(lambda x: x['soil_moisture']['bottom'])
        log['last_watering_time_top'] = pd.to_datetime(log['log'].apply(lambda x: x['last_watering_time']['top']))
        log['last_watering_time_bottom'] = pd.to_datetime(log['log'].apply(lambda x: x['last_watering_time']['bottom']))
        log['light_1'] = log['log'].apply(lambda x: 1 if x['light']['1'] == 'ON' else -1)
        log['light_2'] = log['log'].apply(lambda x: 2 if x['light']['2'] == 'ON' else -1)
        log['fan_top'] = log['log'].apply(lambda x: x['fan']['top'])
        log['fan_bottom'] = log['log'].apply(lambda x: x['fan']['bottom'])

        window_short_columns = ['thermometer_top', 'thermometer_bottom', 'thermometer_external', 'co2', 'humidity',
                                'fan_top', 'fan_bottom']
        window_long_columns = ['soil_moisture_top', 'soil_moisture_bottom']
        log[window_short_columns] = log[window_short_columns].rolling(window=WINDOW_SHORT).mean()
        log[window_short_columns] = log[window_short_columns].apply(lambda x: round(x, 2))
        log[window_long_columns] = log[window_long_columns].rolling(window=WINDOW_LONG).mean()
        log[window_long_columns] = log[window_long_columns].apply(lambda x: round(x, 2))
        log = log.dropna()
        del log['log']
        log = log.groupby(pd.Grouper(key='ts', freq='1min')).last().reset_index()
        return log.sort_values(by='ts')
