API_info = {
    'x-rapidapi-key': "SIGN-UP-FOR-KEY",
    'x-rapidapi-host': "unogsng.p.rapidapi.com"
    }

def filter_list(filters, titles_json):
    url = "https://unogsng.p.rapidapi.com/search"
    response = requests.request("GET", url, headers=API_info, params=filters)
    response = response.text

    title_list = []
    filtered_list = []

    for title in titles_json:
        title_list.append(title["netflixid"])

    for title in response["results"]:
        if title["id"] in title_list:
            filtered_list.append(title["id"])

    return filtered_list