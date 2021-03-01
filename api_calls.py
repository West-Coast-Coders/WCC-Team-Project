import os
import requests
from datetime import datetime, timedelta, date

headers = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
}

def get_expiring(limit:int):
    """Makes an API call to unogsNG to get a list of titles expiring soon. Limit is how many results will be returned."""
    params = {
        # Use a default country code of 78 for USA
        "countrylist": "78",
        # For testing purposes, limit number of returned titles to 5
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


def get_recent(limit:int):
    """Makes an API call to unogsNG to get a list of titles recently added. Limit is how many results will be returned."""

    # Find date of two months ago from date of request
    three_months_ago = date.today() - timedelta(days=90)

    params = {
        # Use a default country code of 78 for USA
        "countrylist": "78",
        "newdate": three_months_ago.isoformat,
        # For testing purposes, limit number of returned titles to 5
        "limit": limit
    }
    
    result_json = requests.get(url='https://unogsng.p.rapidapi.com/search', params=params, headers=headers).json()

    # Save results from initial API call to `output_list`
    output_list = result_json['results']
    
    return output_list