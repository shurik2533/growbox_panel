from flask import Flask, render_template
from datetime import datetime, timedelta

from data import get_log
from plots import get_temperature_plot, get_co2_plot, get_humidity_plot, get_soil_moisture_plot, get_lighting_plot

app = Flask(__name__)


@app.route("/")
def hello_world():
    date_to = datetime.now()
    date_from = date_to - timedelta(days=2)
    df = get_log(date_from, date_to)
    temperature_plot = get_temperature_plot(df)
    co2_plot = get_co2_plot(df)
    humidity_plot = get_humidity_plot(df)
    soil_moisture_plot = get_soil_moisture_plot(df)
    lighting_plot = get_lighting_plot(df)

    return render_template(
        'plots.html',
        temperature_plot=temperature_plot,
        co2_plot=co2_plot,
        humidity_plot=humidity_plot,
        soil_moisture_plot=soil_moisture_plot,
        lighting_plot=lighting_plot,
    )
