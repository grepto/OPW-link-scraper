import re
import random

from bs4 import BeautifulSoup
import requests

USER_AGENT_LIST = [
    # Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    # Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]


SCRAPPING_PREFERENCES = dict(
    yandex = dict(
        url_pattern=lambda x: f'https://yandex.ru/search/?text={x}',
        scrap_rule = lambda soup: [(a['href'], a.find('div', class_='organic__url-text').text) for a in
                                soup.findAll('a', class_='organic__url', attrs={'data-bem': re.compile('^((?!video).)*$')})]
    ),
    google = dict(
        url_pattern=lambda x: f'https://www.google.com/search?q={x}',
        scrap_rule = lambda soup: [(div.a['href'], div.a.h3.span.text) for div in soup.find_all('div', class_='r')]
    ),
    other = dict(
        scrap_rule = lambda soup: [(a['href'], a.text) for a in soup.find_all('a', href=re.compile('^(http|https)://'))]
    ),
)


def get_search_url(domain, query):
    return SCRAPPING_PREFERENCES[domain]['url_pattern'](query)

def get_scrapping_func(domain='other'):
    return SCRAPPING_PREFERENCES[domain]['scrap_rule']


def get_links(url, scrapping_rule):

    user_agent = random.choice(USER_AGENT_LIST)
    headers = {'User-Agent': user_agent}

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')

    return scrapping_rule(soup)


def find_links(search_engine, query, limit=None, is_recursively=False):
    url = get_search_url(search_engine, query)
    search_engine_scrapping_rule = get_scrapping_func(search_engine)

    links = get_links(url, search_engine_scrapping_rule)
    result_list = links

    if is_recursively:
        page_scrapping_rule = get_scrapping_func()

        for link in links:
            if limit and len(result_list) > limit:
                break
            page_links = get_links(link[0], page_scrapping_rule)
            result_list.extend(page_links)

    return result_list[:limit]




url = 'https://www.google.com/search?q=рекурсия'
url2 = 'https://yandex.ru/search/?text=дерево'
url3 = 'https://ru.wikipedia.org/wiki/дерево'

search_engine = 'google'
query = 'лапоть'
url = get_search_url(search_engine, 'лапоть')
scrapping_rule = get_scrapping_func(search_engine)
limit = 100
is_recursively=True

finded_links = find_links(search_engine, query, limit, is_recursively)

print(*finded_links, sep='\n')


# scrapping_rule = get_scrapping_func()
# page_links = get_links('https://ru.wiktionary.org/wiki/%D0%BB%D0%B0%D0%BF%D0%BE%D1%82%D1%8C', scrapping_rule)
# print(page_links)
