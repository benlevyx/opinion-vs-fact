from urllib.parse import urlparse

from opinion import utils


urlpatterns = utils.load_urlpatterns()


def url_is_opinion(url: str) -> bool:
    """Return true if the URL is an opinion article.
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lstrip('www.')
    path = parsed.path
    pattern = urlpatterns(domain)
    return utils.regex_match(pattern, path)


def html_is_opinion(html: str) -> bool:
    """Return true if the HTML is an opinion article.
    """
    pass


def text_is_opinion(text: str) -> bool:
    """Return true if the text is an opinion article.
    """
    pass
