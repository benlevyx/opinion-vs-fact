import json
import re

from .config import data


def load_urlpatterns() -> dict:
    return json.load((data / 'urlpatterns.json').open('r'))


def regex_match(regex, text) -> bool:
    """Return True if the text matches the regex
    """
    return bool(re.match(regex, text))
