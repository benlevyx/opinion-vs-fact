import pytest

from opinion import api, article


mc = api.get_api_conn()


def test_api_simple():
    story_id = 502218391
    jsonResponse = mc.story(story_id, raw_1st_download=True, text=True)
    assert article.is_opinion(jsonResponse)
