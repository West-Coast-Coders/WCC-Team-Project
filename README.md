# Netflix Guide
<i>Make School SPD 1.3 Team Project</i>

Built by a team of Make School students, Netflix Guide is a new way to search and browse titles on Netflix. 

On Netflix Guide, users can search for titles across Netflix's entire global catalog. This allows users who circumvent regional restrictions with VPNs to see the country availability for each title. Additionally, users can see the audio and subtitle languages for each title in each country that it is available in to watch. 

Netflix Guide also presents two lists for titles available in the U.S.: Recently Added and Expiring Soon. Recently Added titles were added to Netflix in the past 90 days, and Expiring Soon titles are slated to leave Netflix within 1-2 months. Each title in the Expiring Soon list includes an expiration date. Each of these pages also has sliders at the top to filter results by certain parameters (such as release year, runtime, and IMDb rating). 

## Back-end Technology

Netflix Guide uses the [unogsNG API](https://rapidapi.com/unogs/api/unogsng) for all of its data. The API calls and routes are handled using the `flask` and `requests` Python libraries, and the results are displayed with Jinja2 templates. The code for the sliders for the filters was obtained from [this StackOverflow post](https://stackoverflow.com/questions/4753946/html5-slider-with-two-inputs-possible/64612997#64612997). We also used [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) for CSS styling.

## Front-end Technology

NetflixGuide uses flexbox and bootstrap for all of its UI.  

## Deployment

Start using Netflix Guide today! Visit [here](https://wcc-netflix-guide.herokuapp.com).

The homepage displays the search bar at the top, along with two carousels below: one for Recently Added, and one for Expiring Soon. Each carousel scrolls through nine thumbnail images of titles belonging to their respective list. Clicking on the list section (Recently Added or Expiring Soon) will lead to a new page displaying all of the titles in a grid for that list. If the user clicks on a thumbnail image on any page, it will lead to a new page displaying all of the details for that title (name, release year, runtime, synopsis, maturity level, IMDb rating, Metascore rating, country availability, genres, etc.). 
