import aiohttp
import asyncio
from aiohttp import TCPConnector
from bs4 import BeautifulSoup

async def fetch_page(session, url):
    async with session.get(url) as response:
        return await response.text()

async def fetch_article(session, url):
    async with session.get(url) as response:
        return await response.text()

async def news_parser(page: int, sport: str):
    url = "https://www.*****.ru/news/"
    url_temp = url
    full_news = []
    links_list = []
    sport_len = len(sport) + 1

    
    connector = TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []

        
        for num in range(2, page + 2):
            tasks.append(fetch_page(session, url_temp))

            url_temp = url + f'page{num}/'

   
        pages_content = await asyncio.gather(*tasks)

      
        for content in pages_content:
            soup = BeautifulSoup(content, 'html.parser')
            articles = soup.find_all('div', class_='articles-item')

            for article in articles:
                link = article.find('a')['href']
                full_url = 'https://www.*****.ru' + link

                if link[1:sport_len] == sport:
                    links_list.append(full_url)

    
        article_tasks = []
        for link_elem in links_list:
            article_tasks.append(fetch_article(session, link_elem))

        article_contents = await asyncio.gather(*article_tasks)

        
        for content, link_elem in zip(article_contents, links_list):
            soup_el = BeautifulSoup(content, 'html.parser')
            article_text_div = soup_el.find('div', class_='article-text clearfix')

            if article_text_div:
                article_text = article_text_div.get_text(strip=True)
                if article_text:
                    full_news.append((link_elem, article_text[8:]))

    return full_news


async def main():
    my_news = await news_parser(page=10, sport='hock')
    for news in my_news:
        print(news[0])
        print(news[1])


asyncio.run(main())
