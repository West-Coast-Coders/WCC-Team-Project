import requests
import os

API_info = {
    'x-rapidapi-key': os.getenv('API_KEY'),
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
    }

def filter_list(filters, titles):
    filtered_titles = titles

    if filters['type']:
        temp = []
  
        for title in filtered_titles:
            if filters['type'] == title['vtype']:
                temp.append(title)
        
        filtered_titles = temp


    if filters['start_year'] and filters['end_year']:
        temp = []

        for title in filtered_titles:
            if int(title['year']) > int(filters['start_year']) and \
            int(title['year']) < int(filters['end_year']):
                temp.append(title)
        
        filtered_titles = temp


    if filters['start_rating'] and filters['end_rating']:
        temp = []

        for title in filtered_titles:
            if float(title['imbdrating']) > float(filters['start_rating']) and \
            float(title['imbdrating']) < float(filters['end_rating']):
                temp.append(title)
        
        filtered_titles = temp


    if filters['min_runtime'] and filters['max_runtime']:
        temp = []

        for title in filtered_titles:
            if int(title['netflixruntime']) > int(filters['min_runtime']) and \
            int(title['netflixruntime']) < int(filters['max_runtime']):
                temp.append(title)
        
        filtered_titles = temp


    print("filtering completed")
    return filtered_titles