import requests
from bs4 import BeautifulSoup

def news_parser(page: int, sport: str):
    url = "https://www.*****.ru/news/"
    url_temp = url
    full_news = list()
    links_list = list()
    sport_len = len(sport) + 1

    for num in range(2, page + 2):

        response = requests.get(url_temp)
        html_content = response.content
        soup = BeautifulSoup(html_content, 'html.parser')
        articles = soup.find_all('div', class_='articles-item')

        url_temp = url + f'page{num}/'

        for article in articles:
            link = article.find('a')['href']
            full_url = 'https://www.****.ru' + link

            if link[1:sport_len] == sport:
                links_list.append(full_url)


    for link_elem in links_list:

        resp_elem = requests.get(link_elem)
        elem_content = resp_elem.content
        soup_el = BeautifulSoup(elem_content, 'html.parser')
        article_text_div = soup_el.find('div', class_='article-text clearfix')
       
      if article_text_div:
            article_text = article_text_div.get_text(strip=True)
            if article_text :
                full_news.append((link_elem,article_text[8:]))
    return full_news


my_news = news_parser(page=10,
                      sport= 'hock')
for news in my_news:
    print(news[0])
    print(news[1])
