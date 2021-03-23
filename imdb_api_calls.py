import os
import requests
from scraping import scrape_digitalTrends, get_arriving_titles, get_leaving_titles

# load_dotenv()

headers = {
    'x-rapidapi-key': os.getenv('IMDB_API_KEY'),
    'x-rapidapi-host': "imdb8.p.rapidapi.com"
}


def get_arriving(service, limit:int):
    """Makes an API call to IMDB API to get a list of titles expiring soon on input service."""

    # Create empty list to hold results from GET request for results dictionary
    results_dict_list = []

    # Iterate through the list of tuples returned from the scraping module (with some limit)
    for title_tuple in get_arriving_titles(scrape_digitalTrends(service))[0: (limit - 1)]:
        # The full title is the third element in each tuple
        full_title = title_tuple[2]
        # Remove all characters to the right of any comma and open parenthesis
        stripped_title = full_title.rsplit(",")[0].rsplit("(")[0]
        # If "Season" is included after any colon, then remove that part after the colon
        colon_split_list = stripped_title.rsplit(":")
        if len(colon_split_list) > 1 and "Season" in colon_split_list[1]:
            stripped_title = colon_split_list[0]

        params = {
            # Pass in the title name for the single parameter
            "q": stripped_title
        }

        # Send GET request for 'find' results
        result_json = requests.get(url='https://imdb8.p.rapidapi.com/title/find', params=params, headers=headers).json()

        if 'results' in result_json:
            if ('id' in result_json['results'][0]) and ('image' in result_json['results'][0]):

                imdb_id = result_json['results'][0]["id"][7:]
                imdb_id = imdb_id[:-1]

                # Store only the IMDB id and the image URL of the first result from the output JSON
                output_dict = {
                    "id": imdb_id, 
                    "img": result_json['results'][0]["image"]["url"], 
                    "title": full_title,
                    "arrivaldate": title_tuple[1]
                    }
                # Add the first result from above to return list
                results_dict_list.append(output_dict)


    return results_dict_list

def get_expiring(service, limit:int):
    """Makes an API call to IMDB API to get a list of titles expiring soon on input service."""

    # Create empty list to hold results from GET request for results dictionary
    results_dict_list = []

    # Iterate through the list of tuples returned from the scraping module (with some limit)
    for title_tuple in get_leaving_titles(scrape_digitalTrends(service))[0: (limit - 1)]:
        # The full title is the third element in each tuple
        full_title = title_tuple[2]
        # Remove all characters to the right of any comma and open parenthesis
        stripped_title = full_title.rsplit(",")[0].rsplit("(")[0]
        # If "Season" is included after any colon, then remove that part after the colon
        colon_split_list = stripped_title.rsplit(":")
        if len(colon_split_list) > 1 and "Season" in colon_split_list[1]:
            stripped_title = colon_split_list[0]

        params = {
            # Pass in the title name for the single parameter
            "q": stripped_title
        }

        # Send GET request for 'find' results
        result_json = requests.get(url='https://imdb8.p.rapidapi.com/title/find', params=params, headers=headers).json()
        
        if 'results' in result_json:
            if ('id' in result_json['results'][0]) and ('image' in result_json['results'][0]):

                imdb_id = result_json['results'][0]["id"][7:]
                imdb_id = imdb_id[:-1]
                
                # Store only the IMDB id and the image URL of the first result from the output JSON
                output_dict = {
                    "id": imdb_id, 
                    "img": result_json['results'][0]["image"]["url"],
                    "title": full_title,
                    "expiredate": title_tuple[1]
                    }
                # Add the first result from above to return list
                results_dict_list.append(output_dict)

    return results_dict_list
