import re
import requests
from bs4 import BeautifulSoup as bs

def search_movie(titletype, genre):
  STATS = []
  header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
  url = f"https://www.imdb.com/search/title/?title_type={titletype}&num_votes=25000,&genres={genre}&sort=user_rating,desc"
  page = requests.get(url, headers=header)
  soup = bs(page.text, 'html.parser')

  movies = soup.find_all("div", class_="lister-item-content")
  for movie in movies:
    title = movie.find('a').text
    url = "https://www.imdb.com"+movie.a['href']
    STATS.append({
      'title': title,
      'url': url,
    })
  return STATS

# if __name__ == '__main__':
#   search_movie('feature', 'comedy')
