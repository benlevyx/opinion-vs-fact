from urllib.parse import urlparse

from opinion import utils


urlpatterns = utils.load_urlpatterns()


def url_is_opinion(url: str) -> bool:
    """Return true if the URL is an opinion article.
    """
    parsed = urlparse(url)
    domain = parsed.netloc.lstrip('www.')
    path = parsed.path

    all_pattern = urlpatterns.get('all')
    if utils.regex_match(all_pattern, path):
        return True

    site_pattern = urlpatterns.get(domain, None)
    if site_pattern:
        return utils.regex_match(site_pattern, path)


def html_is_opinion(html: str) -> bool:
    """Return true if the HTML is an opinion article.
    """
    pass


def text_is_opinion(text: str) -> bool:
    """Return true if the text is an opinion article.
    """
    pass
