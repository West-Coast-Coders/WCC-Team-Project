import os
import requests
import re
from bs4 import BeautifulSoup as bs

digital_trends_services = ["hulu", "hbo", "amazon-prime", "disney-plus", "netflix", "peacock"]

# Arriving and leaving: HBO, Hulu, Netflix
# Only arriving: Disney+, Amazon Prime (split into Movies and TV), Peacock

def scrape_digitalTrends(service):
    """Parses the HTML code of a webpage.
    
    Returns: a list of three-tuples consisting of title names, release years, and expiration/addition dates
    """

    # Load the webpage content using the input link
    page = requests.get(f"https://www.digitaltrends.com/movies/new-on-{service}/")

    # Convert to a beautiful soup object
    soup = bs(page.content, features="html5lib")

    # Save actual content of page from the article section
    content = soup.find("article", attrs={"id": "dt-post-content"})

    return content


def arriving_titles(soup_article):

    # Instantiate empty list that will be filled and returned later
    arriving_list = []

    arriving = soup_article.find_all("h3", string=re.compile("(N|n)ew"))

    for date in arriving:
        arrival_date = date.text
        for title in date.find_all("li"):
            title_split = title.split("(")
            arriving_title_name = title_split[0]
            arriving_title_extra = title_split[1].strip(")")
            # if arriving_title_extra.isdigit():
            #     release_year = arriving_title_extra
            arriving_list.append((arriving_title_name, arrival_date, arriving_title_extra))

    return arriving_list
    


