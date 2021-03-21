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

imdb_headers = {
    'x-rapidapi-key': os.getenv('IMDB_API_KEY'),
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
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


@app.route('/title/<titleid>')
def title_details(titleid):
    """Displays all the details for an individual title on a full page, along with related titles."""

    related_titles = []
    # Initially setting details to 'None' to be able to check whether or not the title information should come from the Netflix
    # or IMDB API
    details = None

    # Making relevant API calls based on whether or not the title ID is a Netflix ID or IMDB ID
    if not titleid.startswith('tt'):
        # Send a GET request for the details of a specific title using its unique Netflix ID
        details = requests.get(
            url='https://unogsng.p.rapidapi.com/title', 
            params={'netflixid': titleid}, 
            headers=netflix_headers
            ).json()["results"][0]

        # Send a GET request for the country availability related to a specific title using its unique Netflix ID
        countries = requests.get(
            url='https://unogsng.p.rapidapi.com/titlecountries', 
            params={'netflixid': titleid}, 
            headers=netflix_headers
            ).json()["results"]

        # Send a GET request for the genres related to a specific title using its unique Netflix ID
        genres = requests.get(
            url='https://unogsng.p.rapidapi.com/titlegenres', 
            params={'netflixid': titleid}, 
            headers=netflix_headers
            ).json()["results"]

        # Send a GET request for the IMDB ID of the Netflix title
        titleid = requests.get(
            url="https://imdb8.p.rapidapi.com/title/find", 
            params={"q": details['title']}, 
            headers=imdb_headers
            ).json()['results'][0]['id'][7:]

    else:
        # Send a GET request for the info of a specific title using its unique IMDB ID
        imdb_title_info = requests.get(
            url="https://imdb8.p.rapidapi.com/title/get-overview-details", 
            params={"tconst": titleid}, 
            headers=imdb_headers
            ).json()

    watch_options = requests.get(
            url="https://imdb8.p.rapidapi.com/title/get-meta-data", 
            params={"ids": titleid}, 
            headers=imdb_headers
            ).json()[titleid]['waysToWatch']

    print(watch_options)

    # Send a GET request for title ID's related to the searched title
    related_title_ids = requests.get(
        url="https://imdb8.p.rapidapi.com/title/get-more-like-this", 
        params={"tconst": str(titleid)}, 
        headers=imdb_headers
        ).json()

    # Send a GET request for a trailer related to the searched title
    video = requests.get(
        url="https://imdb8.p.rapidapi.com/title/get-videos", 
        params={"tconst": titleid}, 
        headers=imdb_headers
        ).json()['resource']

    if 'videos' in video:
        video['videos'][0]['id'] =  video['videos'][0]['id'][9:]

    # Properly formatting the related title ID's , getting their basic info, and appending that info to the 'related_titles'
    # list
    for title in related_title_ids:
        title = title[7:]
        title_info = requests.get(
            url="https://imdb8.p.rapidapi.com/title/get-base", 
            params={"tconst": title}, 
            headers=imdb_headers
            ).json()

        title_info['id'] = title_info['id'][7:]
        title_info['id'] = title_info['id'][:-1]

        related_titles.append(title_info)

    # Rendering the title info page with all needed information variables based on if the title came from the Netflix API or
    # IMDB API
    if details:
        # Send the resulting dictionary to a new page to display the details
        return render_template(
            'title_details.html', 
            details=details, 
            countries=countries, 
            genres=genres, 
            related_titles=related_titles, 
            video=video,
            watch_options=watch_options
            )
    else:
        return render_template(
            'title_details.html', 
            related_titles=related_titles, 
            title_info=imdb_title_info, 
            video=video,
            watch_options=watch_options 
            )
        
@app.route('/services/netflix')
def netflix():
    output_list_1, title_details_1 = get_expiring(9)
    output_list_2 = get_recent(9)
    return render_template("netflix.html", output_list_1=output_list_1, title_details_1=title_details_1, 
                                         output_list_2=output_list_2)


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