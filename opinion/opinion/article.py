import json

from .classifier import (url_is_opinion, html_is_opinion,
                         text_is_opinion)
from .error import ArticleError


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
