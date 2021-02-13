import jinja2
# import matplotlib
# import matplotlib.pyplot as plt
import os
import pytz
import requests
import sqlite3

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
from io import BytesIO
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# API Info
# Get the API key from the '.env' file
load_dotenv()
headers = {
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

    params = {
        "countrylist": country,
        # For testing purposes, limit number of returned titles to 5
        "limit": 5
    }
    
    result_json = requests.get(url='https://unogsng.p.rapidapi.com/expiring', params=params, headers=headers).json()

    # Save results from initial API call to `output_list`
    output_list = result_json['results']

    # Create empty list to hold results from GET request for title details
    title_details = []

    for i in range(len(output_list)):
        # Select the netflixid for each title from the returned JSON object
        netflixid = output_list[i]['netflixid']
        # Send a GET request for title details and add the resulting dictionary to the title_details dictionary
        title_details.append(requests.get(url='https://unogsng.p.rapidapi.com/title', params={'netflixid': netflixid}, headers=headers).json()["results"][0])

    # Print the results of the API call
    # pp.pprint(result_json)

    # context = {
    #     'expiredate': result_json['results'][i]['expiredate'].strftime('%A, %B %d, %Y'),
    #     'countrycode': result_json['results']['countrycode'],
    #     'netflixid': result_json['results']['netflixid'],
    #     'title': result_json['results']['title']
    # }

    # return render_template('expirations.html', **result_json)
    return render_template('expirations.html', result_json = result_json, title_details = title_details)


if __name__ == '__main__':
    app.run(debug=True)
