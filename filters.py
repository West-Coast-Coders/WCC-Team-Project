import requests
import os


def filter_list(filters, titles_info, list_results):

    def show_only_filtered(filtered_titles_info, list_results):
        titles_info_titles = []
        results_titles = list_results
        j = 0

        for title_info in filtered_titles_info:
            titles_info_titles.append(title_info['title'])

        for i in range(len(list_results)):
            result = list_results[i-j]

            if result['title'] not in titles_info_titles:
                results_titles.remove(result)
                j += 1

        return results_titles


    filtered_titles = titles_info

    if filters['type']:
        temp = []
  
        for title in filtered_titles:
            if filters['type'] == title['vtype']:
                temp.append(title)
        
        filtered_titles = temp


    if filters['start_year'] and filters['end_year']:
        temp = []

        for title in filtered_titles:
            if int(title['year']) >= int(filters['start_year']) and \
            int(title['year']) <= int(filters['end_year']):
                temp.append(title)
        
        filtered_titles = temp


    if filters['start_rating'] and filters['end_rating']:
        temp = []

        for title in filtered_titles:
            if float(title['imbdrating']) >= float(filters['start_rating']) and \
            float(title['imbdrating']) <= float(filters['end_rating']):
                temp.append(title)
        
        filtered_titles = temp


    if filters['min_runtime'] and filters['max_runtime']:
        temp = []

        for title in filtered_titles:
            if int(title['netflixruntime']) >= int(filters['min_runtime']) and \
            int(title['netflixruntime']) <= int(filters['max_runtime']):
                temp.append(title)
        
        filtered_titles = temp

    filtered_list_results = show_only_filtered(filtered_titles, list_results)
    final_results = [filtered_titles, filtered_list_results]
    return final_results
