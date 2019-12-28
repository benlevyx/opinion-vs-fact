import csv

import pytest

import opinion
from opinion import config

with (config.tests / 'test_urls.csv').open('r') as csvfile:
    test_urls = [row for row in csv.reader(csvfile)]


def test_nytimes():
    for url, is_opinion in test_urls:
        a = opinion.Article(url=url)
        is_opinion = is_opinion == 'yes'
        assert a.is_opinion() == is_opinion
