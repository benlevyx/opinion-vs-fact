import csv

import pytest

from opinion import config, article


def test_simple_pos():
    # This isn't working at the moment. WaPo isn't the best tester
    _run_test('https://www.washingtonpost.com/most-of-us-are-bad-at-apologizing-the-pope-just-showed-us-how-its-done/2020/01/02/711aea90-2d99-11ea-bcb3-ac6482c4a92f_story.html',
              'washingtonpost-pos.html', True)


def test_multilevel_pos():
    _run_test('https://www.newsweek.com/corporate-social-responsibility-sham-opinion-1480082',
              'newsweek-pos.html', True)


def test_contains_pos():
    _run_test('https://observer.com/2019/07/democrat-leadership-fighting-legal-weed-2020-election/',
              'observer-pos.html', True)


def test_simple_neg():
    _run_test('https://www.washingtonpost.com/weather/2020/01/02/amid-bush-fire-crisis-this-weekend-may-bring-australia-its-most-dangerous-fire-weather-conditions-yet/?hpid=hp_hp-more-top-stories_australia-forecast-320pm-1-duplicate%3Ahomepage%2Fstory-ans',
              'washingtonpost-neg.html', False)


def test_multilevel_neg():
    _run_test('https://www.newsweek.com/taiwan-president-vows-ensure-stability-national-army-after-military-chief-dies-helicopter-1480021',
              'newsweek-neg.html', False)


def test_contains_neg():
    _run_test('https://observer.com/2020/01/warren-buffett-berkshire-hathaway-decline-tiffany-acquisition-before-lvmh-deal/',
              'observer-neg.html', False)


def _run_test(url: str, fpath: str, is_opinion: bool) -> None:
    with (config.tests / fpath).open('r') as f:
        html = f.read().strip()
    jsonResp = {
        'url': url,
        'raw_first_download_file': html,
        'text': '',
        'stories_id': 0
    }
    output = article.is_opinion(jsonResp)
    print(output)
    assert output[0]['is_opinion'] == is_opinion
