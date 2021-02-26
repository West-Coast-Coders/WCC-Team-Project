import jinja2
# import matplotlib
# import matplotlib.pyplot as plt
import os
import pytz
import requests
import sqlite3

from pprint import PrettyPrinter
from datetime import datetime, timedelta, date
# from dateutil.relativedelta import *
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

@app.route('/country-id')
def countrycode():
    url = "https://unogsng.p.rapidapi.com/countries"

    headers = {
        'x-rapidapi-key': "2e473e01d3msh716bf7f4c960569p101e32jsn9d46bb61a5dc",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)

    print(response.text)

@app.route('/expiring-soon')
def expiring():
    """Displays results for titles that are expiring soon from Netflix."""
    # Use 'request.args' to retrieve the country code from the query parameters
    # country = request.args.get('countrycode')

    params = {
        # Use a default country code of 78 for USA
        "countrylist": "78",
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

    return render_template('expirations.html', result_json = result_json, title_details = title_details)

@app.route('/recently-added')
def recently_added():
    """Displays results for titles that were added onto Netflix in the past three months."""
    # Use 'request.args' to retrieve the country code from the query parameters
    # country = request.args.get('countrycode')

    # Find date of two months ago from date of request
    three_months_ago = date.today() - timedelta(days=90)

    params = {
        # Use a default country code of 78 for USA
        "countrylist": "78",
        "newdate": three_months_ago.isoformat,
        # For testing purposes, limit number of returned titles to 5
        "limit": 5
    }
    
    result_json = requests.get(url='https://unogsng.p.rapidapi.com/search', params=params, headers=headers).json()

    # Save results from initial API call to `output_list`
    results = result_json['results']

    return render_template('recently_added.html', results = results)

@app.route('/title/<netflixid>')
def title_details(netflixid):
    """Displays all the details for an individual title on a full page."""

    # Send a GET request for the details of a specific title using its unique Netflix ID
    details = requests.get(url='https://unogsng.p.rapidapi.com/title', params={'netflixid': netflixid}, headers=headers).json()["results"][0]

    # Send a GET request for the country availability related to a specific title using its unique Netflix ID
    countries = requests.get(url='https://unogsng.p.rapidapi.com/titlecountries', params={'netflixid': netflixid}, headers=headers).json()["results"]

    # Send a GET request for the genres related to a specific title using its unique Netflix ID
    genres = requests.get(url='https://unogsng.p.rapidapi.com/titlegenres', params={'netflixid': netflixid}, headers=headers).json()["results"]

    # Send the resulting dictionary to a new page to display the details
    return render_template('title_details.html', details=details, countries=countries, genres=genres)

# Create a function to separate string of languages into a list



"""
{
            "country": "Argentina ",
            "id": 21,
            "countrycode": "AR"
        },
        {
            "country": "Australia ",
            "id": 23,
            "countrycode": "AU"
        },
        {
            "country": "Belgium ",
            "id": 26,
            "countrycode": "BE"
        },
        {
            "country": "Brazil ",
            "id": 29,
            "countrycode": "BR"
        },
        {
            "country": "Canada ",
            "id": 33,
            "countrycode": "CA"
        },
        {
            "country": "Switzerland ",
            "id": 34,
            "countrycode": "CH"
        },
        {
            "country": "Germany ",
            "id": 39,
            "countrycode": "DE"
        },
        {
            "country": "France ",
            "id": 45,
            "countrycode": "FR"
        },
        {
            "country": "United Kingdom",
            "id": 46,
            "countrycode": "GB"
        },
        {
            "country": "Mexico ",
            "id": 65,
            "countrycode": "MX"
        },
        {
            "country": "Netherlands ",
            "id": 67,
            "countrycode": "NL"
        },
        {
            "country": "Sweden ",
            "id": 73,
            "countrycode": "SE"
        },
        {
            "country": "United States",
            "id": 78,
            "countrycode": "US"
        },
        {
            "country": "Iceland ",
            "id": 265,
            "countrycode": "IS"
        },
        {
            "country": "Japan ",
            "id": 267,
            "countrycode": "JP"
        },
        {
            "country": "Portugal ",
            "id": 268,
            "countrycode": "PT"
        },
        {
            "country": "Italy ",
            "id": 269,
            "countrycode": "IT"
        },
        {
            "country": "Spain ",
            "id": 270,
            "countrycode": "ES"
        },
        {
            "country": "Czech Republic ",
            "id": 307,
            "countrycode": "CZ"
        },
        {
            "country": "Greece ",
            "id": 327,
            "countrycode": "GR"
        },
        {
            "country": "Hong Kong ",
            "id": 331,
            "countrycode": "HK"
        },
        {
            "country": "Hungary ",
            "id": 334,
            "countrycode": "HU"
        },
        {
            "country": "Israel ",
            "id": 336,
            "countrycode": "IL"
        },
        {
            "country": "India ",
            "id": 337,
            "countrycode": "IN"
        },
        {
            "country": "South Korea",
            "id": 348,
            "countrycode": "KR"
        },
        {
            "country": "Lithuania ",
            "id": 357,
            "countrycode": "LT"
        },
        {
            "country": "Poland ",
            "id": 392,
            "countrycode": "PL"
        },
        {
            "country": "Romania ",
            "id": 400,
            "countrycode": "RO"
        },
        {
            "country": "Russia",
            "id": 402,
            "countrycode": "RU"
        },
        {
            "country": "Singapore ",
            "id": 408,
            "countrycode": "SG"
        },
        {
            "country": "Slovakia ",
            "id": 412,
            "countrycode": "SK"
        },
        {
            "country": "Thailand ",
            "id": 425,
            "countrycode": "TH"
        },
        {
            "country": "Turkey ",
            "id": 432,
            "countrycode": "TR"
        },
        {
            "country": "South Africa",
            "id": 447,
            "countrycode": "ZA"
        }"""




# FILTERS TESTING:
# @app.route('/process-filters', methods=['POST'])
# def process():
#     title_type = request.form['type']
#     start_year = request.form['start_year']
#     order_by = request.form['order_by']
#     audiosubtitle_andor = request.form['audiosubtitle_andor']
#     start_rating = request.form['start_rating']
#     end_rating = request.form['end_rating']
#     subtitle = request.form['subtitle']
#     country_list = request.form['country_list']
#     audio = request.form['audio']
#     country_andorunique = request.form['country_andorunique']
#     end_year = request.form['end_year']
#     current_list = request.form['current_list']

#     filters = {
#         "type":title_type
#         "start_year":start_year,
#         "orderby":order_by,
#         "audiosubtitle_andor":audiosubtitle_andor,
#         "start_rating":start_rating,
#         "end_rating":end_rating,
#         "subtitle":"english",
#         "countrylist":country_list,
#         "audio":audio,
#         "country_andorunique":country_andorunique,
#         "end_year":end_year
#     }



if __name__ == '__main__':
    app.run(debug=True)
