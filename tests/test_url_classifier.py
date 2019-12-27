import csv

import pytest

import opinion


test_urls = csv.reader('test_urls.csv').readlines()


def test_nytimes():
    for url, is_opinion in test_urls:
        a = opinion.Article(url=url)
        is_opinion = is_opinion == 'yes'
        assert a.is_opinion() == is_opinion
