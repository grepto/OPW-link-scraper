#!/usr/bin/env python3

import argparse
import logging.config

from envparse import env

from scrapper import find_links

parser = argparse.ArgumentParser(description='Link scrapper')
parser.add_argument('query', action='store', help='Query to search')
parser.add_argument('engine', action='store', choices=['yandex', 'google'],
                    help='Witch search engine use to find query links')
parser.add_argument('-l', type=int, action='store', dest='limit', default=100, help='Limit links in result')
parser.add_argument('-r', action='store_true', dest='is_recursively', default=False, help='Recursively scrapping')

args = parser.parse_args()

if __name__ == '__main__':

    env.read_envfile()

    log_config = {
        'version': 1,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'base_Formatter',
                'level': env('LOG_LEVEL'),
            }
        },
        'loggers': {
            'scrapper': {
                'handlers': ['console'],
                'level': env('LOG_LEVEL'),
            }
        },
        'formatters': {
            'base_Formatter': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
            },
        }
    }

    logging.config.dictConfig(log_config)

    found_links = find_links(args.engine, args.query, args.limit, args.is_recursively)
    for (link, title) in found_links:
        print(title, link, sep=' - ')  # noqa
