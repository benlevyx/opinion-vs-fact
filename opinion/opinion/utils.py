import json
import re

from .config import data, apikey


def load_urlpatterns() -> dict:
    return json.load((data / 'urlpatterns.json').open('r'))


def regex_match(regex, text) -> bool:
    """Return True if the text matches the regex
    """
    return bool(re.match(regex, text))


def get_apikey() -> str:
    """Get my API keys (saved in project root)
    """
    with apikey.open('r') as f:
        key = f.read().strip('\n')
    return key
