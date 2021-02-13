import jinja2
import matplotlib
import matplotlib.pyplot as plt
import os
import pytz
import requests
import sqlite3
import simplejson

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file, redirect, url_for
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from filters import filter_list


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()
API_info = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
    }
# print(API_KEY)


# Settings for image endpoint
# Written with help from http://dataviztalk.blogspot.com/2016/01/serving-matplotlib-plot-that-follows.html
# matplotlib.use('agg')
# plt.style.use('ggplot')

# my_loader = jinja2.ChoiceLoader([
#     app.jinja_loader,
#     jinja2.FileSystemLoader('data'),
# ])
# app.jinja_loader = my_loader

pp = PrettyPrinter(indent=4)


################################################################################
## ROUTES
################################################################################


@app.route('/')
def home():
    """Displays the homepage"""
    return render_template("index.html")

@app.route('/expiring-soon', methods=['GET', 'POST'])
def expiring(result_json=None):
    """Displays results for titles that are expiring soon from Netflix."""
    # Use 'request.args' to retrieve the country code from the query parameters
    country = request.args.get('countrycode')

    url = 'https://unogsng.p.rapidapi.com/expiring'

    params = {
        "countrylist": country
    }
    
    if not result_json:
        result_json = requests.get(url, params=params, headers=API_info).json()

    # Save results from initial API call to `output_list`
    output_list = result_json['results']

    # Create empty dictionary to hold results from GET request for title details
    title_details = {}

    # for i in range(len(output_list)):
    #     # Select the netflixid for each title from the returned JSON object
    #     netflixid = output_list[i]['netflixid']
    #     # Send a GET request for title details and add the resulting dictionary to the title_details dictionary
    #     title_details += requests.get(url="https://unogsng.p.rapidapi.com/title", params={'netflixid': netflixid}, headers=API_info).json()["results"][0]

    # Print the results of the API call
    # pp.pprint(result_json)

    # context = {
    #     'expiredate': result_json['results'][i]['expiredate'].strftime('%A, %B %d, %Y'),
    #     'countrycode': result_json['results']['countrycode'],
    #     'netflixid': result_json['results']['netflixid'],
    #     'title': result_json['results']['title']
    # }

    if request.method == 'POST':
        filters_json = request.json
        print(filters_json)
        # filters = simplejson.loads(filters_json)
        filtered_list = filter_list(filters_json, result_json)

        print(filtered_list)

        return redirect(url_for('expiring', result_json = filtered_list))

    # return render_template('expirations.html', **result_json)
    return render_template('expirations.html', result_json = result_json, title_details = title_details)


if __name__ == '__main__':
    app.run(debug=True)
