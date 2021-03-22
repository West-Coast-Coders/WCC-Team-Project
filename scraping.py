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
    content = soup.find("article")

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
    arriving_sections = soup_article.find_all("h2", string=re.compile("((N|n)ew)|((A|a)rriving)"))
    # Find all of the date sections (h3 elements)
    arriving_items = []
    # Find all of the list items under each date section (ul elements)
    arriving_items_list = []
    for section in arriving_sections:
        for section_sibling in section.find_next_siblings():
            if section_sibling.name == "h3":
                arriving_items.append(section_sibling)
            if section_sibling.name == "ul":
                arriving_items_list.append(section_sibling)
            # Skip over the next big or small heading unless it's a section denoting TV/Movies
            if section_sibling.name == "h2" or section_sibling.name == "h4":
                if section_sibling.string == "TV" or section_sibling.string == "Movies":
                    continue
                else:
                    break
    # print(arriving_items_list[0])
    # print(arriving_items)
    while "\n" in arriving_items_list:
        arriving_items_list.remove("\n")


    # Iterate through each date 
    for i in range(len(arriving_items)):
        # Save the date text
        arrival_date = arriving_items[i].string
        # Iterate through each list under each date
        # print(arriving_items_list[i])
        for title in arriving_items_list[i]:
            # Ignore new-line characters in the list
            if title == "\n":
                continue
            # print(title)
            # Save full title with extraneous details
            full_title = title.get_text()
            # print(full_title)
            # Strip everything after a dash, comma, or open parenthesis to keep only the name
            title_split = full_title.rsplit("(")[0].rsplit(",")[0].rsplit(":")[0]
            # title_split = [full_title]
            # The name is the first part of the line
            arriving_title_name = title_split
            # Add the new three-tuple with the name, leaving date, and title with extra info to the return list
            arriving_list.append((arriving_title_name, arrival_date, full_title))

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
                leaving_items.append(section_sibling)
            if section_sibling.name == "ul":
                leaving_items_list.append(section_sibling)
            # Skip over the next big or small heading unless it's a section denoting TV/Movies
            if section_sibling.name == "h2" or section_sibling.name == "h4":
                if section_sibling.string == "TV" or section_sibling.string == "Movies":
                    continue
                else:
                    break
    while "\n" in leaving_items_list:
        leaving_items_list.remove("\n")

    # Iterate through each date 
    for i in range(len(leaving_items)):
        # Save the date text
        leaving_date = leaving_items[i].string
        # Iterate through each list under each date
        # print(leaving_items_list)
        for title in leaving_items_list[i]:
            # Ignore new-line characters in the list
            if title == "\n":
                continue
            # Save full title with extraneous details
            full_title = title.string
            # Strip everything after a dash, comma, or open parenthesis to keep only the name
            title_split = full_title.rsplit("(")[0].rsplit(",")[0].rsplit(":")[0]
            # The name is the first part of the line
            leaving_title_name = title_split
            # Add the new three-tuple with the name, leaving date, and title with extra info to the return list
            leaving_list.append((leaving_title_name, leaving_date, full_title))
        
    return leaving_list
    


# SUCCESS
# print(arriving_titles(scrape_digitalTrends("hulu"))) 
# SUCCESS
# print(leaving_titles(scrape_digitalTrends("hulu")))

# SUCCESS
# print(arriving_titles(scrape_digitalTrends("hbo")))
# SUCCESS
# print(leaving_titles(scrape_digitalTrends("hbo")))

# SUCCESS
# print(arriving_titles(scrape_digitalTrends("amazon-prime")))

# SUCCESS
# print(arriving_titles(scrape_digitalTrends("disney-plus")))

# SUCCESS
# print(arriving_titles(scrape_digitalTrends("netflix")))
# SUCCESS
# print(leaving_titles(scrape_digitalTrends("netflix")))

# SUCCESS
# print(arriving_titles(scrape_digitalTrends("peacock")))
