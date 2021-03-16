# NetflixGuide
<i>Make School SPD 1.3 Team Project</i>

Built by a team of Make School students, NetflixGuide is a new way to search and browse titles on Netflix. 

On NetflixGuide, users can search for titles across Netflix's entire global catalog. This allows users who circumvent regional restrictions with VPNs to see the country availability for each title. Additionally, users can see the audio and subtitle languages for each title in each country that it is available in to watch. 

NetflixGuide also presents two lists for titles available in the U.S.: Recently Added and Expiring Soon. Recently Added titles were added to Netflix in the past 90 days, and Expiring Soon titles are slated to leave Netflix within 1-2 months. Each title in the Expiring Soon list includes an expiration date. Each of these pages also has sliders at the top to filter results by certain parameters (such as release year, runtime, and IMDb rating). 

## Back-end Technology

NetflixGuide uses the [unogsNG API](https://rapidapi.com/unogs/api/unogsng) for all of its data. The API calls and routes are handled using the `flask` and `requests` Python libraries, and the results are displayed with Jinja2 templates. The code for the sliders for the filters was obtained from [this StackOverflow post](https://stackoverflow.com/questions/4753946/html5-slider-with-two-inputs-possible/64612997#64612997). We also used [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) for CSS styling.

## Front-end Technology

NetflixGuide uses flexbox and bootstrap for all of its UI.  

## Deployment

Start using NetflixGuide today! Visit [here](https://wcc-netflix-guide.herokuapp.com).

The homepage displays the search bar at the top, along with two carousels below: one for Recently Added, and one for Expiring Soon. Each carousel scrolls through nine thumbnail images of titles belonging to their respective list. Clicking on the list section (Recently Added or Expiring Soon) will lead to a new page displaying all of the titles in a grid for that list. If the user clicks on a thumbnail image on any page, it will lead to a new page displaying all of the details for that title (name, release year, runtime, synopsis, maturity level, IMDb rating, Metascore rating, country availability, genres, etc.). 

Home page:
<img width="1437" alt="Home Page" src="https://user-images.githubusercontent.com/37927005/109781105-7a3fc600-7bbc-11eb-8690-0ec6a002b6a5.png">

Leaving Soon page:
<img width="1437" alt="Leaving Soon" src="https://user-images.githubusercontent.com/37927005/109781043-6c8a4080-7bbc-11eb-9e44-5e9833bdc6cb.png">

Recently Added page:
<img width="1437" alt="Recently Added" src="https://user-images.githubusercontent.com/37927005/109781576-e4f10180-7bbc-11eb-8866-473633250931.png">

Example Search Results page:
<img width="1438" alt="Search Query" src="https://user-images.githubusercontent.com/37927005/109781791-0ce06500-7bbd-11eb-9431-a60c4189ecaa.png">

Title Details page:
<img width="1436" alt="Title Details" src="https://user-images.githubusercontent.com/37927005/109781868-21bcf880-7bbd-11eb-95c4-c4b34c04a7f1.png">



