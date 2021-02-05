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
    # Use 'request.args' to retrieve the country code from the query parameters
    country = request.args.get('countrycode')

    url = 'https://unogsng.p.rapidapi.com/expiring'

    params = {
        "countrylist": country
    }

    headers = {
        'x-rapidapi-key': "391142fa44msh629bf4333450dbdp15459ajsn08b13a9231cf",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
    }
    
    result_json = requests.get(url, params=params, headers=headers).json()

    # Print the results of the API call
    pp.pprint(result_json)

    context = {
        'expiredate': result_json['results']['expiredate'].strftime('%A, %B %d, %Y'),
        'countrycode': result_json['results']['countrycode'],
        'netflixid': result_json['results']['netflixid'],
        'title': result_json['results']['title']
    }

    return render_template('results.html', **context)


if __name__ == '__main__':
    app.run(debug=True)
