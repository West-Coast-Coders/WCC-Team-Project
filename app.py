import jinja2
import matplotlib
import matplotlib.pyplot as plt
import os
import pytz
import requests
import sqlite3
import json
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
    """Search function to browse avalible movies on nexflix."""

    return render_template('home.html')

# def get_letter_for_units(units):
#     """Returns a shorthand letter for the given units."""
#     return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/search_results')
def results():
    """Search Result"""
    title = request.args.get('title')


    url = "https://unogsng.p.rapidapi.com/search"
    params = {
        "start_year":"1972","orderby":"rating","subtitle":"english","query":title,"audio":"english","offset":"0"
    }

    headers = {
    'x-rapidapi-key': "5a290bcfe7mshae1b67802e67c81p1499cfjsneb78dae05462",
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
    }

    result_json = requests.get(url, headers=headers, params=params).json()

    pp.pprint(result_json)

    context = {
        'title': result_json["results"][0]["title"],
        'synopsis': result_json["results"][0]["synopsis"],
        'year': result_json["results"][0]["year"]
    }
    return render_template('results.html', **context)


if __name__ == '__main__':
    app.run(debug=True)


    # {% for item in range(response["ITEMS"]|length) %}
    # <ul>
    #     <li>Name: {{ response["ITEMS"][item]['title'] }}</li>
    #     <li>Image: {{ response["ITEMS"][item]['image'] }}</li>
    #     <li>synopsis: {{response["ITEMS"][item]['synopsis'] }}</li>
    # </ul>
    # {% endfor %}