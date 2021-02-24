import requests
import os


def filter_list(filters, titles_info, list_results):
    """Takes in a list of specific titles, another list with details about each title, and finally, filter
       parameters. Returns a list with both list filtered. """

    def show_only_filtered(filtered_titles_info, list_results):
        """Filters the main list of titles based on what was filtered from the list containing the title details"""
        # List of only the titles taken from the list of titles info
        titles_info_titles = []
        results_titles = list_results
        # The variable j is to properly index the for loop on line 20. Without this, the for loop would be cut short due
        # to each time the loop runs, there is a possibility of an element getting removed from the list that we are looping
        # over, cutting the loop short. In other words, this variable is to ensure that the loop runs for the amount of the 
        # original length of the list.
        j = 0

        # Populating titles_info_titles with only the title field from the list of title info (filtered_titles_info parameter)
        for title_info in filtered_titles_info:
            titles_info_titles.append(title_info['title'])

        # Checking if every title in the main list is in the filtered title list; If not, remove that title from the main list
        for i in range(len(list_results)):
            result = list_results[i-j]

            if result['title'] not in titles_info_titles:
                results_titles.remove(result)
                j += 1

        # Returning the finished filtered main list
        return results_titles


    filtered_titles = titles_info
    

    # The following statements below is where the actual filtering of the titles take place. The filtered list starts out 
    # with the full list, in theory, getting smaller and smaller as it moves down the filter checks.

    if filters['type']:
        temp = []
  
        for title in filtered_titles:
            if filters['type'] == title['vtype']:
                temp.append(title)
        
        filtered_titles = temp


    # Filtering year range
    temp = []

    for title in filtered_titles:
        if int(float(title['year'])) >= int(float(filters['start_year'])) and \
        int(float(title['year'])) <= int(float(filters['end_year'])):
            temp.append(title)
    
    filtered_titles = temp


    # Filtering IMDB rating range
    temp = []

    for title in filtered_titles:
        if not title['imdbrating']:
            temp.append(title)
        elif float(title['imdbrating']) >= float(filters['start_rating']) and \
        float(title['imdbrating']) <= float(filters['end_rating']):
            temp.append(title)
    
    filtered_titles = temp


    # Filtering runtime range
    temp = []

    for title in filtered_titles:
        if title['netflixruntime'] == 0:
            temp.append(title)
        elif int(title['netflixruntime']) >= int(filters['min_runtime']) and \
        int(title['netflixruntime']) <= int(filters['max_runtime']):
            temp.append(title)
    
    filtered_titles = temp

    # Now that the list of titles is filtered, pass that onto the show_only_filtered function to additionally filter the main
    # list
    filtered_list_results = show_only_filtered(filtered_titles, list_results)
    # Putting the two filtered lists into one list to return
    final_results = [filtered_titles, filtered_list_results]
    return final_results
