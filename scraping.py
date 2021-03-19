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
    # Find all of the date sections (h3 elements)
    arriving_items = []
    # Find all of the list items under each date section (ul elements)
    arriving_items_list = []
    for section in arriving_sections:
        for section_sibling in section.find_next_siblings():
            if section_sibling.name == "h3":
                arriving_items += section_sibling
            if section_sibling.name == "ul":
                arriving_items_list += section_sibling
            if section_sibling.name == "h2":
                break
        # for date_section in section.find_next_siblings("h3"):
        #     arriving_items += date_section
        # print(arriving_items_list)

    # Iterate through each date 
    for i in range(len(arriving_items)):
        # Save the date text
        arrival_date = arriving_items[i].string
        # Iterate through each list under each date
        for title in arriving_items_list[i]:
            # Ignore new-line characters in the list
            if title == "\n":
                continue
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
    # Find all of the date sections (h3 elements)
    leaving_items = []
     # Find all of the list items under each date section (ul elements)
    leaving_items_list = []
    for section in leaving_sections:
        for section_sibling in section.find_next_siblings():
            if section_sibling.name == "h3":
                leaving_items += section_sibling
            if section_sibling.name == "ul":
                leaving_items_list += section_sibling
            if section_sibling.name == "h2":
                break
    

    # Iterate through each date 
    for i in range(len(leaving_items)):
        # Save the date text
        leaving_date = leaving_items[i].string
        # Iterate through each list under each date
        for title in leaving_items_list[i]:
            # Ignore new-line characters in the list
            if title == "\n":
                continue
            # Split the line by opening parentheses
            title_split = title.text.split("(")
            # The name is the first part of the line
            leaving_title_name = title_split[0]
            # Extra info is contained in the rest of the line
            leaving_title_extra = title_split[1].strip(")")
            # If the first character of the extra info is a letter, then 
            # add that piece to the name and save the release year as extra info (if the year is included)
            if leaving_title_extra[0].isalpha():
                leaving_title_name += ("(" + leaving_title_extra)
                if len(title_split) > 2:
                    leaving_title_extra = title_split[2].strip(")")
            # Add the new three-tuple with the name, leaving date, and extra info to the return list
            leaving_list.append((leaving_title_name, leaving_date, leaving_title_extra))
        
    return leaving_list
    


print(arriving_titles(scrape_digitalTrends("hulu")))
print(leaving_titles(scrape_digitalTrends("hulu")))

# print(arriving_titles(scrape_digitalTrends("hbo")))
# print(leaving_titles(scrape_digitalTrends("hbo")))

# print(arriving_titles(scrape_digitalTrends("amazon-prime")))
# print(leaving_titles(scrape_digitalTrends("amazon-prime")))

print(arriving_titles(scrape_digitalTrends("disney-plus")))
print(leaving_titles(scrape_digitalTrends("disney-plus")))