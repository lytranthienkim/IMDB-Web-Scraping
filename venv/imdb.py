import requests
import bs4
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd


HEADERS = {'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'}
url = 'https://www.imdb.com/chart/top/?ref_=nv_mv_250'
response = requests.get(url, headers=HEADERS)
soup = bs4.BeautifulSoup(response.content, 'html.parser')


MAIN_URL = 'https://www.imdb.com'

def imdb(soup):
    imdb_source_url = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base')
    imdb_href = [link['href'] for link in imdb_source_url.select('a.ipc-title-link-wrapper')]
    imdb_href_join = [urljoin(MAIN_URL, imdb_href) for imdb_href in imdb_href]
    return imdb_href_join
imdb_movie = imdb(soup)


movie_250_list = []
NUM = 0
for movie in range(len(imdb_movie)):
    try:
        response = requests.get(imdb_movie[movie], headers=HEADERS)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.content, 'html.parser')

        def movie_title(soup):
            extract_movie_title = soup.find('h1', {'data-testid':'hero__pageTitle'}).text.strip()
            return extract_movie_title
        extract_movie_title = movie_title(soup)

        def country_pl(soup):
            country = soup.find('li', {'data-testid': 'title-details-origin'})
            extract_country = country.find('a', class_='ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link').text
            return extract_country
        extract_country = country_pl(soup)

        def runtime(soup):
            get_runtime = soup.find('div', {'data-testid': 'title-techspecs-section'})
            if get_runtime:
                time = get_runtime.find('div', class_='ipc-metadata-list-item__content-container')
                if time:
                    extract_runtime = time.text.strip()
                return extract_runtime
        extract_runtime = runtime(soup)

        def imdb(soup):
            get_imdb = soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'})
            if get_imdb:
                get_score = get_imdb.find('span')
                if get_score:
                    extract_get_score = re.search(r'^([\d.]+)', get_score.get_text(strip=True))
                    if extract_get_score:
                        extract_imdb_score = extract_get_score.group(1)
                        return extract_imdb_score
        extract_imdb_score = imdb(soup)

        def meta_score(soup):
            get_meta_score = soup.find('span', class_='sc-b0901df4-0 bcQdDJ metacritic-score-box')
            if get_meta_score:
                extract_meta_score = get_meta_score.text.strip()
                return extract_meta_score
        extract_meta_score = meta_score(soup)
       
        def award(soup):
            oscars_award = soup.find('ul', class_='ipc-metadata-list ipc-metadata-list--dividers-none sc-b45a339a-2 cEeAGk ipc-metadata-list--base')
            if oscars_award:
                extract_award = oscars_award.get_text(strip=True)
            return extract_award
        extract_award = award(soup)

        def genre(soup):
            genres = soup.find_all('a', class_='ipc-chip ipc-chip--on-baseAlt', href=lambda x: x and 'genres=' in x)
            get_genres = [genre.find('span', class_='ipc-chip__text').get_text(strip=True) for genre in genres]
            extract_movie_genres = ', '.join(get_genres)
            return extract_movie_genres
        extract_movie_genres = genre(soup)

        def release(soup):
            release_dates = soup.find_all('a', class_='ipc-link ipc-link--baseAlt ipc-link--inherit-color')
            for date in release_dates:
                extract_release_date = re.search(r'(\d{4})', date.get_text(strip=True))
                if extract_release_date:
                    extract_release_date = extract_release_date.group(1)
                    break
            return extract_release_date
        extract_release_date = release(soup)

        def presentation(soup):
            extract_presentation = soup.find('span', {'data-testid': 'plot-l'}).get_text(strip=True)
            return extract_presentation
        extract_presentation = presentation(soup)

        def review(soup):
            get_review = soup.find('div', {'data-testid':'review-overflow'})
            if get_review:
                extract_review = get_review.text.strip()
            return extract_review
        extract_review = review(soup)

        def video(soup):
            url_video = soup.find('a', {'class':'ipc-title-link-wrapper'})
            if url_video:
                href_value = url_video.get('href')
                extract_video = [urljoin(MAIN_URL, href_value)]
            return extract_video
        extract_video = video(soup)

        NUM += 1
        movie_250_list.append({
            ' ': NUM,
            'Movie': extract_movie_title,
            'Countries of origin': extract_country,
            'Runtime': extract_runtime,
            'IMDb rating': extract_imdb_score,
            'Metascore': extract_meta_score,
            'Award': extract_award,
            'Genre': extract_movie_genres,
            'Release date': extract_release_date,
            'Presentation': extract_presentation,
            'Featured reviews': extract_review,
            'Video': extract_video
        })
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


imdb_movie = pd.DataFrame(movie_250_list, columns = [' ', 'Movie', 'Countries of origin', 'Runtime', 'IMDb rating', 'Metascore', 'Award', 'Genre', 'Release date', 'Presentation', 'Featured reviews', 'Video'])
print(imdb_movie)