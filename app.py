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
from api_calls import get_expiring, get_recent
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
    output_list_1, title_details_1 = get_expiring(9)
    output_list_2 = get_recent(9)
    return render_template("index.html", output_list_1=output_list_1, title_details_1=title_details_1, 
                                         output_list_2=output_list_2)

@app.route('/country-id')
def countrycode():
    url = "https://unogsng.p.rapidapi.com/countries"

    headers = {
        'x-rapidapi-key': "2e473e01d3msh716bf7f4c960569p101e32jsn9d46bb61a5dc",
        'x-rapidapi-host': "unogsng.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers)

    print(response.text)  

@app.route('/expiring-soon', methods=['GET', 'POST'])
def expiring():
    """Displays results for titles that are expiring soon from Netflix."""
    # Use 'request.args' to retrieve the country code from the query parameters
    # country = request.args.get('countrycode')

    
    
    # Save results from initial API call to `output_list` and get addtional title details from "get_expiring"
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
            'min_runtime': (request.form['min-runtime'] * 60 ),
            'max_runtime': (request.form['max-runtime'] * 60 )
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
    output_list = get_recent(5)
    

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



if __name__ == '__main__':
    app.run(debug=True)
