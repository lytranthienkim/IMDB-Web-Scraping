# SCRAPING IMDB DATA USING BEAUTIFULSOUP

Hi! In this simple scraping, I will introduce how to crawl movie data at IMDb.com using BeautifulSoup. Imagine that we have a list of 'top 250 movies' and we're interested in watching one of them. However, it has lots of information to reach out to. That is why we need a CSV document to streamline this process that fetches only the movie name, countries of origin, runtime, ...

**Beautiful Soup** serves as a library designed to simplify the extraction of information from web pages. It operates on an HTML or XML parser, offering Pythonic expressions for navigating, searching, and modifying the parsed tree structure.

## Goal
  
The conclusive outcomes will be structured into a data frame, encompassing the following elements: the movie name, countries of origin, runtime, IMDb rating, Metascore, awards, genre, release date, presentation, featured reviews, and the video's URL.

## Virtual Enviroment

We need to download virtual environment packages to import necessary modules.

**>> Venv** 

    macbook@user-name file-name % python3 -m venv venv
    macbook@user-name file-name % source venv/bin/activate
    (venv) macbook@user-name scraping imdb % pip list
  > ...
  Package    Version
    ---------- -------
    pip        19.2.3 
    setuptools 41.2.0 
    WARNING: You are using pip version 19.2.3, however version 23.3.1 is available.
    You should consider upgrading via the 'pip install --upgrade pip' command.
   
    (venv) macbook@user-name scraping imdb % pip install --upgrade pip
   > ...
    Collecting pip
      Using cached https://files.pythonhosted.org/packages/47/6a/453160888fab7c6a432a6e25f8afe6256d0d9f2cbd25971021da6491d899/pip-23.3.1-py3-none-any.whl
    Installing collected packages: pip
      Found existing installation: pip 19.2.3
        Uninstalling pip-19.2.3:
          Successfully uninstalled pip-19.2.3
    Successfully installed pip-23.3.1

**>> Request**

    pip3 install requests
> ...
    Collecting requests
      Using cached requests-2.31.0-py3-none-any.whl.metadata (4.6 kB)
    Collecting charset-normalizer<4,>=2 (from requests)
      Using cached charset_normalizer-3.3.2-cp38-cp38-macosx_10_9_x86_64.whl.metadata (33 kB)
    Collecting idna<4,>=2.5 (from requests)
      Downloading idna-3.6-py3-none-any.whl.metadata (9.9 kB)
    Collecting urllib3<3,>=1.21.1 (from requests)
      Using cached urllib3-2.1.0-py3-none-any.whl.metadata (6.4 kB)
    Collecting certifi>=2017.4.17 (from requests)
      Downloading certifi-2023.11.17-py3-none-any.whl.metadata (2.2 kB)
    Using cached requests-2.31.0-py3-none-any.whl (62 kB)
    Downloading certifi-2023.11.17-py3-none-any.whl (162 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 162.5/162.5 kB 1.1 MB/s eta 0:00:00
    Using cached charset_normalizer-3.3.2-cp38-cp38-macosx_10_9_x86_64.whl (121 kB)
    Downloading idna-3.6-py3-none-any.whl (61 kB)
       ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 61.6/61.6 kB 1.5 MB/s eta 0:00:00
    Using cached urllib3-2.1.0-py3-none-any.whl (104 kB)
    Installing collected packages: urllib3, idna, charset-normalizer, certifi, requests
    Successfully installed certifi-2023.11.17 charset-normalizer-3.3.2 idna-3.6 requests-2.31.0 urllib3-2.1.0
    
**>> BeautifulSoup**

    pip3 install beautifulsoup4
   > ...
    Collecting beautifulsoup4
      Using cached beautifulsoup4-4.12.2-py3-none-any.whl (142 kB)
    Collecting soupsieve>1.2 (from beautifulsoup4)
      Using cached soupsieve-2.5-py3-none-any.whl.metadata (4.7 kB)
    Using cached soupsieve-2.5-py3-none-any.whl (36 kB)
    Installing collected packages: soupsieve, beautifulsoup4
    Successfully installed beautifulsoup4-4.12.2 soupsieve-2.5
    
## Import Module
 
 Now, let's import all the necessary modules in program.

    import bs4
    import re
    import pandas as pd
    from bs4 import BeautifulSoup
    from urllib.parse import urljoin

Next, copy the URL of IMDb top list of 250 movies and assign it to the 'url' variable. The **requests.get** method is used to send an **HTTP GET** request to this URL, and the server's response is stored in the variable response. The script utilizes the **BeautifulSoup** library with the '**html.parser'** to parse the HTML content of the response, creating a structured parse tree. This parsed content, represented by the variable soup, can be easily navigated and searched using Beautiful Soup's Pythonic expressions. Overall, the code sets the stage for extracting specific movie-related information from the IMDb webpage. Additionally, the use of **HEADERS** in the request headers helps simulate a browser-like request to avoid potential issues during web scraping. 

    HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'} 
    ## Windows environment: HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
   Why **HEADERS** ? To avoid a **403 error,** commonly referred to as "Forbidden while web scraping. The **Response** will return **Response <200>**  indicates a successful request. 
   
    url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
    response = requests.get(url, headers=HEADERS)
    soup = bs4.BeautifulSoup(response.content, 'html.parser')


## Scraping data

**Method:** scraping 250 URLs of 250 movies, then, accessing each URL to retrieve attributes: [Movie], [Countries of origin], [Runtime], [IMDb rating], [Metascore], [Award], [Genre], [Release date], [Presentation], [Featured reviews], [Video]. 

**In BeautifulSoup:**

- **find_all(arguments)**: returns a ResultSet, which is a list-like object containing all the matching tags found in the parse tree.
- **find(arguments)**: returns a Tag object, representing the first matching tag found in the parse tree.

	    def imdb(soup):
        imdb_source_url = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base')
        imdb_href = [link['href'] for  link  in  imdb_source_url.select('a.ipc-title-link-wrapper')]
        imdb_href_join = [urljoin(MAIN_URL, imdb_href) for  imdb_href  in  imdb_href]
        return imdb_href_join
        imdb_movie = imdb(soup)

   > output:
 ['https://www.imdb.com/title/tt0111161/?ref_=chttp_t_1',
    'https://www.imdb.com/title/tt0068646/?ref_=chttp_t_2',
    'https://www.imdb.com/title/tt0468569/?ref_=chttp_t_3', 
    'https://www.imdb.com/title/tt0071562/?ref_=chttp_t_4',
    'https://www.imdb.com/title/tt0050083/?ref_=chttp_t_5',
    ....
    'https://www.imdb.com/title/tt0099348/?ref_=chttp_t_248',
    'https://www.imdb.com/title/tt4430212/?ref_=chttp_t_249',
    'https://www.imdb.com/title/tt0079470/?ref_=chttp_t_250']

  Sets up an empty list to contain the extracted movie data and initializes a counter variable with value of 0.

	    movie_250_list = []
	    NUM = 0
  
	Iterating through each discovered URL path involves employing a methodology akin to the one detailed earlier, utilizing the HTTP GET method and the Beautiful Soup library. The implementation incorporates a structured try-except block in Python to proactively manage potential exceptions that may arise during code execution. This systematic approach ensures controlled processing of each URL, facilitating graceful error handling.
	
		 try:
		    response = requests.get(imdb_movie[movie], headers=HEADERS)
		    response.raise_for_status()
		    soup = bs4.BeautifulSoup(response.content, 'html.parser')
		    [...]
		 except requests.exceptions.HTTPError as errh:
			  print(f"HTTP Error occurred: {errh}")
		 except requests.exceptions.ConnectionError as errc:
			  print(f"Error Connecting: {errc}")
	     except requests.exceptions.Timeout as errt:
			  print(f"Timeout Error: {errt}")
		 except requests.exceptions.RequestException as err:
		    print(f"Request Exception: {err}")
		 except Exception as e:
		    print(f"An error occurred: {e}")

**What's Python Try - Except :**   In Python's exception handling, the try-except blocks play a crucial role, providing a framework to handle potential errors during code execution. **The try block** encapsulates code susceptible to exceptions, with the interpreter attempting its execution. If an exception arises, the interpreter skips the remaining try block code and directs control to the corresponding **except block**, specifying actions for the encountered exception. Multiple except blocks can address various exception types. If no exceptions occur in the try block, the associated except block is bypassed, contributing to a structured and robust error management approach in Python programming.

## HTML 

- **Movie Title:** : `<h1 textlength="24" data-testid="hero__pageTitle" class="sc-82970163-0 cKbbOg">`

- **Country:** : `<li role="presentation" class="ipc-inline-list__item"><a class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link">` 

-  **Runtime:** : `<div class="ipc-metadata-list-item__content-container">`

-  **IMDb Score:** : `<div data-testid="hero-rating-bar__aggregate-rating" class="sc-acdbf0f3-0 haeNPA rating-bar__base-button"><div class="sc-acdbf0f3-1 kCTJoV">IMDb RATING</div><a class="ipc-btn ipc-btn--single-padding ipc-btn--center-align-content ipc-btn--default-height ipc-btn--core-baseAlt ipc-btn--theme-baseAlt ipc-btn--on-textPrimary ipc-text-button sc-acdbf0f3-2 caaLCv" role="button" tabindex="0" aria-label="View User Ratings" aria-disabled="false" href="/title/tt0111161/ratings/?ref_=tt_ov_rt"><span class="ipc-btn__text">`

-  **Meta Score:** `<span class="sc-b0901df4-0 bcQdDJ metacritic-score-box">`

-  **Award:** `<ul class="ipc-metadata-list ipc-metadata-list--dividers-none sc-b45a339a-2 cEeAGk ipc-metadata-list--base"`

-  **Genre:** `<a class="ipc-chip ipc-chip--on-baseAlt" role="button" tabindex="0" aria-disabled="false" href="/search/title?genres=drama&amp;explore=title_type,genres&amp;ref_=tt_ov_inf"><span class="ipc-chip__text">`

-  **Release:** `<a class="ipc-link ipc-link--baseAlt ipc-link--inherit-color" role="button" tabindex="0" aria-disabled="false" href="/title/tt0111161/releaseinfo?ref_=tt_ov_rdat">1994</a>`

-  **Presentation:** `<span role="presentation" data-testid="plot-l" class="sc-466bb6c-1 dWufeH">`

-  **Review:** `<div class="ipc-overflowText ipc-overflowText--listCard ipc-overflowText--height-long ipc-overflowText--long ipc-overflowText--click ipc-overflowText--base" role="button" data-testid="review-overflow">`

- **Video:** `<a href="/title/tt0111161/videogallery/?ref_=tt_vi_sm" class="ipc-title-link-wrapper" tabindex="0">`
	

## Result
  
Generate a Pandas DataFrame by combining all the previously defined functions to scrape information from the top 250 movies on the list.

## Note for viewing
  
- IMDb Top 250 Movies.csv: Open with CSV Editor
