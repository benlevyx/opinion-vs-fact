import csv

import pytest

from opinion import config, Article


def test_simple_pos():
    a = _load_html_as_article('https://www.washingtonpost.com/opinions/most-of-us-are-bad-at-apologizing-the-pope-just-showed-us-how-its-done/2020/01/02/711aea90-2d99-11ea-bcb3-ac6482c4a92f_story.html',
                              'washingtonpost-pos.html')
    assert a.is_opinion()


# def test_multilevel_pos():
#     a = _load_html_as_article('newsweek-pos.html')
#     assert a.is_opinion()


# def test_contains_pos():
#     a = _load_html_as_article('observer-pos.html')
#     assert a.is_opinion()


# def test_simple_neg():
#     a = _load_html_as_article('washingtonpost-neg.html')
#     assert a.is_opinion()


# def test_multilevel_neg():
#     a = _load_html_as_article('newsweek-neg.html')
#     assert a.is_opinion()


# def test_contains_neg():
#     a = _load_html_as_article('observer-neg.html')
#     assert a.is_opinion()


def _load_html_as_article(url: str, fpath: str) -> str:
    with (config.tests / fpath).open('r') as f:
        html = f.read().strip()
        a = Article(url=url, html=html)
        return a
