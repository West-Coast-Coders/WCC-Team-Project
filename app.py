import jinja2
# import matplotlib
# import matplotlib.pyplot as plt
import os
import pytz
import requests
# import sqlite3
import json

from pprint import PrettyPrinter
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file, redirect, url_for
# from io import BytesIO
from filters import filter_list
from netflix_api_calls import netflix_get_expiring, netflix_get_recent
# from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# API Info
# Get the API key from the '.env' file
load_dotenv()
netflix_headers = {
    'x-rapidapi-key': os.getenv('NETFLIX_API_KEY'),
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
}

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
    output_list_1, title_details_1 = netflix_get_expiring(9)
    output_list_2 = netflix_get_recent(9)
    return render_template("index.html", output_list_1=output_list_1, title_details_1=title_details_1, 
                                         output_list_2=output_list_2)

@app.route('/country-id')
def countrycode():
    url = "https://unogsng.p.rapidapi.com/countries"

    response = requests.request("GET", url, headers=netflix_headers)

    print(response.text)  


@app.route('/expiring-soon', methods=['GET', 'POST'])
def expiring():
    """Displays results for titles that are expiring soon from Netflix."""
    # Use 'request.args' to retrieve the country code from the query parameters
    # country = request.args.get('countrycode')

    
    
    # Save results from initial API call to `output_list` and get addtional title details from "get_expiring"
    output_list, title_details = netflix_get_expiring(75)


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


@app.route('/recently-added', methods=['GET', 'POST'])
def recently_added():
    """Displays results for titles that were added onto Netflix in the past three months."""
    # Use 'request.args' to retrieve the country code from the query parameters
    # country = request.args.get('countrycode')

    # Save results from initial API call to `output_list` and get addtional title details from "get_expiring"
    output_list = netflix_get_recent(75)
    

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
       
        filtered_results = filter_list(filters, output_list)

        return render_template('recently_added.html', results = filtered_results)

    return render_template('recently_added.html', results = output_list)


@app.route('/title/<netflixid>')
def title_details(netflixid):
    """Displays all the details for an individual title on a full page."""

    # Send a GET request for the details of a specific title using its unique Netflix ID
    details = requests.get(url='https://unogsng.p.rapidapi.com/title', params={'netflixid': netflixid}, headers=netflix_headers).json()["results"][0]

    # Send a GET request for the country availability related to a specific title using its unique Netflix ID
    countries = requests.get(url='https://unogsng.p.rapidapi.com/titlecountries', params={'netflixid': netflixid}, headers=netflix_headers).json()["results"]

    # Send a GET request for the genres related to a specific title using its unique Netflix ID
    genres = requests.get(url='https://unogsng.p.rapidapi.com/titlegenres', params={'netflixid': netflixid}, headers=netflix_headers).json()["results"]

    # Send the resulting dictionary to a new page to display the details
    return render_template('title_details.html', details=details, countries=countries, genres=genres)


@app.route('/search_results')
def results():
    """Search Result"""
    title = request.args.get('title')


    url = "https://unogsng.p.rapidapi.com/search"
    params = {
        "start_year":"1972","orderby":"rating","query":title,"offset":"0"
    }


    result_json = requests.get(url, headers=netflix_headers, params=params).json()

    # pp.pprint(result_json)
    

    return render_template('results.html', result_json=result_json)


if __name__ == '__main__':
    app.run(debug=True)