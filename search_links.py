#!/usr/bin/env python3

import argparse

from scrapper import find_links

parser = argparse.ArgumentParser(description='Link scrapper')
parser.add_argument('query', action='store', help='Query to search')
parser.add_argument('engine', action='store', choices=['yandex', 'google'], help='Witch search engine use to find query links')
parser.add_argument('-l', type=int, action='store', dest='limit', default=100, help='Limit links in result')
parser.add_argument('-r', action='store_true', dest='is_recursively', default=False, help='Recursively scrapping')

args = parser.parse_args()

if __name__ == '__main__':
    finded_links = find_links(args.engine, args.query, args.limit, args.is_recursively)

    for (link, title) in finded_links:
        print(title, link, sep=' - ')  # noqa
