import csv

import pytest

from opinion import config, Article


def test_simple_pos():
    a = _load_html_as_article('https://www.washingtonpost.com/opinions/most-of-us-are-bad-at-apologizing-the-pope-just-showed-us-how-its-done/2020/01/02/711aea90-2d99-11ea-bcb3-ac6482c4a92f_story.html',
                              'washingtonpost-pos.html')
    assert a.is_opinion()


def test_multilevel_pos():
    a = _load_html_as_article('https://www.newsweek.com/corporate-social-responsibility-sham-opinion-1480082',
                              'newsweek-pos.html')
    assert a.is_opinion()


def test_contains_pos():
    a = _load_html_as_article('https://observer.com/2019/07/democrat-leadership-fighting-legal-weed-2020-election/',
                              'observer-pos.html')
    assert a.is_opinion()


def test_simple_neg():
    a = _load_html_as_article('https://www.washingtonpost.com/weather/2020/01/02/amid-bush-fire-crisis-this-weekend-may-bring-australia-its-most-dangerous-fire-weather-conditions-yet/?hpid=hp_hp-more-top-stories_australia-forecast-320pm-1-duplicate%3Ahomepage%2Fstory-ans',
                              'washingtonpost-neg.html')
    assert not a.is_opinion()


def test_multilevel_neg():
    a = _load_html_as_article('https://www.newsweek.com/taiwan-president-vows-ensure-stability-national-army-after-military-chief-dies-helicopter-1480021',
                              'newsweek-neg.html')
    assert not a.is_opinion()


def test_contains_neg():
    a = _load_html_as_article('https://observer.com/2020/01/warren-buffett-berkshire-hathaway-decline-tiffany-acquisition-before-lvmh-deal/',
                              'observer-neg.html')
    assert not a.is_opinion()


def _load_html_as_article(url: str, fpath: str) -> str:
    with (config.tests / fpath).open('r') as f:
        html = f.read().strip()
        a = Article(url=url, html=html)
        return a
