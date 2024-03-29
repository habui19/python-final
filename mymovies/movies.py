import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import re

def scrape(url):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    headers = {'User-Agent': user_agent}
    response = requests.get(url,headers=headers)
    soup = bs(response.text, 'html.parser')
    return soup

def add_movies(url, self_rating):
    soup = scrape(url)
    p = soup.find('div',{'class':'title_wrapper'})
    #scrapping title (this would give back title + year e.g The Lion King (2019))
    title = p.find('h1')
    i = soup.find('div',{'class':'imdbRating'})
    #scrapping imdb rating
    imdb_rating = i.find('span',{'itemprop':'ratingValue'})
    s = soup.find('div',{'class':'subtext'})
    #scrapping movie duration
    duration = s.find('time').text.strip()
    #scrapping genre
    genre = s.find('a')

    data = []

    #change time as objects to time
    duration = duration.replace('h','')
    duration = duration.replace('min','')
    duration = datetime.strptime(duration, '%H %M')

    data = [title.text.strip(), genre.text, imdb_rating.text, self_rating, duration]
    return data

def most_frequent(List): 
    return max(set(List), key = List.count) 

def show_rec(genre):
    #recommendations based on the most genre that has self rating above or equal to 6
    url = f'https://www.imdb.com/search/title/?genres={genre}'
    #scrapping best feature movies based on genres
    soup = scrape(url)

    l = soup.find('div',{'class':'lister-list'})
    #scrapping title from the above url
    titles = l.find_all('div',{'class':'lister-item-content'})

    recommendations = [title.find('h3').text.strip() for title in titles]

    return recommendations