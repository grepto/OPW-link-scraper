import re

import requests
from bs4 import BeautifulSoup

from user_agent import get_user_agent

SCRAPPING_PREFERENCES = dict(
    yandex=dict(
        url_pattern=lambda x: f'https://yandex.ru/search/?text={x}',
        scrap_rule=lambda soup: [(a['href'], a.find('div', class_='organic__url-text').text) for a in
                                 soup.findAll('a', class_='organic__url',
                                              attrs={'data-bem': re.compile('^((?!video).)*$')})]
    ),
    google=dict(
        url_pattern=lambda x: f'https://www.google.com/search?q={x}',
        scrap_rule=lambda soup: [(div.a['href'], div.a.h3) for div in soup.find_all('div', class_='r')]
    ),
    other=dict(
        scrap_rule=lambda soup: [(a['href'], a.text) for a in soup.find_all('a', href=re.compile('^(http|https)://'))]
    ),
)

SEARCH_ENGINE_REQUEST_HEADERS = {
    'User-Agent': get_user_agent()
}


class CaptchaError(Exception):
    pass


def get_search_url(domain, query):
    return SCRAPPING_PREFERENCES[domain]['url_pattern'](query)


def get_scrapping_func(domain='other'):
    return SCRAPPING_PREFERENCES[domain]['scrap_rule']


def get_links(url, scrapping_rule):
    """Getting search result page html code """

    headers = SEARCH_ENGINE_REQUEST_HEADERS
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    try:
        links = scrapping_rule(soup)
    except AttributeError:
        raise CaptchaError('Bot warning mode was activated in search engine. Please wait a few minutes and try again')
    return links


def find_links(search_engine, query, limit=None, is_recursively=False):
    """Links and annotation extraction"""

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
