import os
import requests
import re
from bs4 import BeautifulSoup as bs

digital_trends_services = ["hulu", "hbo", "amazon-prime", "disney-plus", "netflix", "peacock"]

# Arriving and leaving: HBO, Hulu, Netflix
# Only arriving: Disney+, Amazon Prime (split into Movies and TV), Peacock


# Pseudocode
"""
Iterate through tags until h2 found
Iterate through h3 tags until h2 found again
Iterate through list items under each h3

"""


def scrape_digitalTrends(service):
    """
    Grabs the HTML code of a Digital Trends new/expiring webpage.
    Input: a string parameter indicating the streaming service to plug into the URL.
    Returns: a Beautiful Soup object containing the body content of the webpage used for parsing.
    """

    # Load the webpage content using the input link
    page = requests.get(f"https://www.digitaltrends.com/movies/new-on-{service}/")

    # Convert to a beautiful soup object
    soup = bs(page.content, features="html5lib")

    # Save actual content of page from the article section
    content = soup.find("article", attrs={"id": "dt-post-content"})

    return content


def arriving_titles(soup_article):
    """
    Parses the HTML code of a Digital Trends webpage for titles that are arriving soon.
    Input: a Beautiful Soup object containing the body content of the webpage used for parsing.
    Returns: a list of three-tuples consisting of title name, addition date, and extra name info.
    """

    # Instantiate empty list that will be filled and returned later
    arriving_list = []

    # Find all the sections with arriving titles
    arriving_sections = soup_article.find_all("h2", string=re.compile("(N|n)ew"))
    # Find all of the date sections
    arriving_items = []
    for date_section in arriving_sections:
        arriving_items += date_section.find_all("h3")

    # Iterate through each date 
    for date in arriving_items:
        # Save the date text
        arrival_date = date.text
        # Iterate through each bullet point
        for title in date.find_all("li"):
            # Split the line by opening parentheses
            title_split = title.text.split("(")
            # The name is the first part of the line
            arriving_title_name = title_split[0]
            # Extra info is contained in the rest of the line
            arriving_title_extra = title_split[1].strip(")")
            # If the first character of the extra info is a letter, then 
            # add that piece to the name and save the release year as extra info (if the year is included)
            if arriving_title_extra[0].isalpha():
                arriving_title_name += ("(" + arriving_title_extra)
                if len(title_split) > 2:
                    arriving_title_extra = title_split[2].strip(")")
            # Add the new three-tuple with the name, arrival date, and extra info to the return list
            arriving_list.append((arriving_title_name, arrival_date, arriving_title_extra))

    return arriving_list


def leaving_titles(soup_article):
    """
    Parses the HTML code of a Digital Trends webpage for titles that are leaving soon.
    Input: a Beautiful Soup object containing the body content of the webpage used for parsing.
    Returns: a list of three-tuples consisting of title name, expiration date, and extra name info.
    """

    # Instantiate empty list that will be filled and returned later
    leaving_list = []

    # Find all the sections with expiring titles
    leaving_sections = soup_article.find_all("h2", string=re.compile("(L|l)eaving"))
    # Find all of the date sections
    leaving_items = []
    for date_section in leaving_sections:
        leaving_items += date_section.find_all("h3")
    print(leaving_items)

    # Iterate through each date 
    for date in leaving_items:
        print(date)
        # Save the date text
        leaving_date = date.text
        # Iterate through each bullet point
        for title in date.find_all("li"):
            # Split the line by opening parentheses
            title_split = title.text.split("(")
            # The name is the first part of the line
            leaving_title_name = title_split[0]
            # Extra info is contained in the rest of the line
            leaving_title_extra = title_split[1].strip(")")
            # If the first character of the extra info is a letter, then 
            # add that piece to the name and save the release year as extra info
            if leaving_title_extra[0].isalpha():
                leaving_title_name += ("(" + leaving_title_extra)
                if len(title_split) > 2:
                    leaving_title_extra = title_split[2].strip(")")
            # Add the new three-tuple with the name, expiration date, and extra info to the return list
            leaving_list.append((leaving_title_name, leaving_date, leaving_title_extra))
            print("new tuple")

    return leaving_list
    


# print(arriving_titles(scrape_digitalTrends("hulu")))
print(leaving_titles(scrape_digitalTrends("hulu")))

# print(arriving_titles(scrape_digitalTrends("hbo")))
# print(leaving_titles(scrape_digitalTrends("hbo")))

# print(arriving_titles(scrape_digitalTrends("amazon-prime")))
# print(leaving_titles(scrape_digitalTrends("amazon-prime")))

# print(arriving_titles(scrape_digitalTrends("disney-plus")))
# print(leaving_titles(scrape_digitalTrends("disney-plus")))