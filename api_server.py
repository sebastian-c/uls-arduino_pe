from flask import Flask

exec(open("temperature_average.py").read())

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Welcome to this webserver! Please try the following endpoints: /poitiers or other site</p>"

@app.route('/<sensor_location>')
def show_sensor_location(sensor_location):
    
    try:
        sensor_temperature = all_temps[str.lower(sensor_location)]
    except KeyError:
        return f'Could not find sensor location: {sensor_location}'
    return f'Sensor_location: {sensor_location}<br>Average_temperature: {all_temps[str.lower(sensor_location)]}'
