import jinja2
import matplotlib
import matplotlib.pyplot as plt
import os
import pytz
import requests
import sqlite3

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()
API_KEY = os.getenv('API_KEY')
print(API_KEY)


# Settings for image endpoint
# Written with help from http://dataviztalk.blogspot.com/2016/01/serving-matplotlib-plot-that-follows.html
matplotlib.use('agg')
plt.style.use('ggplot')

my_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('data'),
])
app.jinja_loader = my_loader

pp = PrettyPrinter(indent=4)


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/expiring-soon')
def expiring():
    """Displays results for titles that are expiring soon from Netflix."""
    # Use 'request.args' to retrieve the city & units from the query parameters
    city = request.args.get('city')
    units = request.args.get('units')

    url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        # Unique API key
        'appid': API_KEY,
        # City name, possible included with state code and country code (comma-separated)
        'q': city,
        # Units of measurement for temperature
        'units': units
    }

    result_json = requests.get(url, params=params).json()

    # Print the results of the API call
    pp.pprint(result_json)

    context = {
        'date': datetime.now().strftime('%A, %B %d, %Y'),
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']).strftime('%I:%M:%S %p'),
        'sunset': datetime.fromtimestamp(result_json['sys']['sunset']).strftime('%I:%M:%S %p'),
        'units_letter': get_letter_for_units(units)
    }

    return render_template('results.html', **context)

def get_min_temp(results):
    """Returns the minimum temp for the given hourly weather objects."""
    # Iterate through the list in search of the minimum hourly temperature
    min_temp = results[0]['temp']
    for i in range(len(results)):
        temp = results[i]['temp']
        # If new lowest temperature is found, set min_temp to it
        if temp < min_temp:
            min_temp = temp
    return min_temp

def get_max_temp(results):
    """Returns the maximum temp for the given hourly weather objects."""
    # Iterate through the list in search of the maximum hourly temperature
    max_temp = results[0]['temp']
    for i in range(len(results)):
        temp = results[i]['temp']
        # If new highest temperature is found, set max_temp to it
        if temp > max_temp:
            max_temp = temp
    return max_temp


if __name__ == '__main__':
    app.run(debug=True)
