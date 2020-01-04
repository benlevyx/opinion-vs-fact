import json
from typing import Tuple, Union, Numeric

from .classifier import (url_is_opinion, html_is_opinion,
                         text_is_opinion)
from .error import ArticleError
from .config import MODEL_VERSION


class Article:
    def __init__(self, url=None, html=None, text=None, jsonResponse=None):
        """Initialize a new Article

        Keyword Arguments:
        -----------------
        url: str, default None
            The URL of the article.
        html: str, default None
            The raw HTML of the article.
        text: str, default None
            The text of the article.
        jsonResponse: dict|str
            The raw response from a call to the Mediacloud Admin API.
        """
        if not any((url, html, text)):
            if not jsonResponse:
                raise ArticleError("Must provide one of (url, html, text, or jsonResponse)")
            if type(jsonResponse) == str:
                jsonResponse = json.load(jsonResponse)
            self.url = jsonResponse.get('url', None)
            self.html = jsonResponse.get('raw_first_download_file', None)
            self.text = jsonResponse.get('story_text', None)
        else:
            self.url = url
            self.html = html
            self.text = text

    def is_opinion(self) -> True:
        """Return True if the article is an opinion article.

        Tries features in this order:
            1. Check URL (using patterns)
            2. Check HTML (using patterns)
            3. Check text (using machine learning)
        """
        if self.url:
            if url_is_opinion(self.url):
                return True
        if self.html:
            if html_is_opinion(self.url, self.html):
                return True
        if self.text:
            return text_is_opinion(self.text)
        return False


def is_opinion(jsonResponse: Union[dict, str]):
    """
    Arguments:
    ----------
    jsonResponse: dict|str
        The raw response from a call to the Mediacloud Admin API.

    Returns:
    --------
    dict: JSON-like object containing story_id as key, and inner_dict with
    information about whether the article is opinion or not.
    """
    story_id, url, html, text = _unpack_json(jsonResponse)
    story_is_opinion, confidence = _is_opinion(url, html, text)
    return _pack_json(story_id, story_is_opinion, confidence)


def _unpack_json(jsonResponse: Union[str, dict]) -> Tuple[str, str, str]:
    """Unpack a raw response from the Mediacloud Admin API into url, html
    and raw text.
    """
    if type(jsonResponse) == str:
        jsonResponse = json.load(jsonResponse)
    story_id = jsonResponse.get('stories_id', None)
    url = jsonResponse.get('url', None)
    html = jsonResponse.get('raw_first_download_file', None)
    text = jsonResponse.get('story_text', None)
    return story_id, url, html, text


def _pack_json(story_id, story_is_opinion, confidence) -> dict:
    """Repack a tuple of params into a JSON-like dict.
    """
    return {
        story_id: {
            'is_opinion': story_is_opinion,
            'confidence': confidence,
            'model_verison': MODEL_VERSION
        }
    }


def _is_opinion(url: str, html: str, text: str) -> Tuple[bool, Numeric]:
    """Return True if the article is an opinion article.

    Tries features in this order:
        1. Check URL (using patterns)
        2. Check HTML (using patterns)
        3. Check text (using machine learning)

    Returns:
    --------
    (is_opinion, confidence)
    """
    if url:
        if url_is_opinion(url):
            return True, 1.0
    if html:
        if html_is_opinion(url, html):
            return True, 1.0
    if text:
        return text_is_opinion(text)
    return False
