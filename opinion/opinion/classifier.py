from lxml import etree

from .utils import load_json_from_data, regex_match, parse_url


urlpatterns = load_json_from_data('urlpatterns.json')
htmlselectors = load_json_from_data('htmlselectors.json')
parser = etree.HTMLParser()


def url_is_opinion(url: str) -> bool:
    """Return true if the URL is an opinion article.
    """
    domain, path = parse_url(url)

    all_pattern = urlpatterns.get('all')
    if regex_match(all_pattern, path):
        return True

    site_pattern = urlpatterns.get(domain, None)
    if site_pattern:
        return regex_match(site_pattern, path)


def html_is_opinion(url: str, html: str) -> bool:
    """Return true if the HTML is an opinion article.
    """
    domain, path = parse_url(url)
    selector = htmlselectors.get(domain, False)
    if not selector:
        return False
    parsed = etree.fromstring(html, parser)
    if len(parsed.cssselect(selector)) > 0:
        return True
    else:
        return False


def text_is_opinion(text: str) -> bool:
    """Return true if the text is an opinion article.
    """
    return False
