import jinja2
# import matplotlib
# import matplotlib.pyplot as plt
import os
import pytz
import requests
import sqlite3
import json

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file, redirect, url_for
from io import BytesIO
from filters import filter_list
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
    """Displays the homepage"""
    output_list, title_details = get_expiring(9)
    return render_template("index.html", output_list=output_list, title_details=title_details)

@app.route('/expiring-soon', methods=['GET', 'POST'])
def expiring(output_list=None):
    """Displays results for titles that are expiring soon from Netflix."""
    # Use 'request.args' to retrieve the country code from the query parameters
    # country = request.args.get('countrycode')

    
    if not output_list:
        # Save results from initial API call to `output_list`
        output_list, title_details = get_expiring(5)


    # Print the results of the API call
    # pp.pprint(result_json)

    if request.method == 'POST':
        filters = {
            'type': request.form['type'],
            'start_year': request.form['start-year'],
            'end_year': request.form['end-year'],
            'start_rating': request.form['start-rating'],
            'end_rating': request.form['end-rating'],
            'min_runtime': request.form['min-runtime'],
            'max_runtime': request.form['max-runtime']
        }
       
        filtered_results = filter_list(filters, title_details, output_list)

        return render_template('expirations.html', output_list = filtered_results[1], title_details = filtered_results[0])

    return render_template('expirations.html', output_list = output_list, title_details = title_details)


def get_expiring(limit:int):
    """Makes an API call to unogsNG to get a list of titles expiring soon. Limit is how many results will be returned."""
    params = {
        "countrylist": "78",
        "limit": limit
    }

    result_json = requests.get(url='https://unogsng.p.rapidapi.com/expiring', params=params, headers=headers).json()
    output_list = result_json['results']

    # Create empty list to hold results from GET request for title details
    title_details = []

    for i in range(len(output_list)):
        # Select the netflixid for each title from the returned JSON object
        netflixid = output_list[i]['netflixid']
        # Send a GET request for title details and add the resulting dictionary to the title_details dictionary
        title_details.append(requests.get(url='https://unogsng.p.rapidapi.com/title', params={'netflixid': netflixid}, headers=headers).json()["results"][0])

    return output_list, title_details



if __name__ == '__main__':
    app.run(debug=True)
