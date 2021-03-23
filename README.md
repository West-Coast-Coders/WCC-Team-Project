# StreamingxGuide
<i>Make School SPD 1.3 and INT 1.3 Team Project</i>

Built by a team of Make School students, StreamingGuide is a new way to search and browse titles on all major streaming platforms. 

On StreamingGuide, users can browse titles arriving soon and leaving soon across Netflix, HBO Max, Hulu, Disney+, Amazon Prime, and Peacock. On Netflix, users can also browse through Netflix's full global catalog. This allows users who circumvent regional restrictions with VPNs to see the country availability for each title. Additionally, users can see the audio and subtitle languages for each title in each country that it is available in to watch. 

StreamingGuide also presents details for each title (such as release year, synopsis, etc.) along with a trailer and a list of related titles. Each title in the Leaving Soon lists includes an expiration date. Each of pages with lists also has sliders at the top to filter results by certain parameters (such as release year, runtime, and IMDb rating). 

## Back-end Technology

StreamingGuide uses the [unogsNG API](https://rapidapi.com/unogs/api/unogsng) for all of its Netflix data. Other data (such as trailers and related titles) are pulled from the [IMDb API](https://rapidapi.com/apidojo/api/imdb8/endpoints). The API calls and routes are handled using the `flask` and `requests` Python libraries, and the results are displayed with Jinja2 templates. The lists of titles that are arriving soon and leaving soon from all of the streaming services besides Netflix were culled from [Digital Trends](https://www.digitaltrends.com/topic/streaming/) with web scraping using the `BeautifulSoup` Python library. The code for the sliders for the filters was obtained from [this StackOverflow post](https://stackoverflow.com/questions/4753946/html5-slider-with-two-inputs-possible/64612997#64612997). We also used 

## Front-end Technology

StreamingGuide uses [Bootstrap](https://getbootstrap.com/docs/4.6/getting-started/introduction/) for its UI.  

## Deployment

Start using StreamingGuide today! Visit [here](https://wcc-streaming-guide.herokuapp.com).

The homepage displays the search bar at the top, along with a drop-down menu at the top-left corner. The titles under each streaming service can be accessed via the drop-down menu or via the cards in the center of the homepage.

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



