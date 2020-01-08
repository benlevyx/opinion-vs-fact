import pytest

from opinion import api, article


mc = api.get_api_conn()


def test_api_url():
    # nytimes.com: 'How Has This Pesticide Not Been Banned?'
    story_id = 1475475904
    _run_test(story_id, True)


def test_api_html():
    story_id = 1387699345
    _run_test(story_id, True)


def _run_test(story_id: int, is_opinion: bool) -> None:
    jsonResponse = mc.story(story_id, raw_1st_download=True)
    assert article.is_opinion(jsonResponse)[story_id]['is_opinion'] == is_opinion
