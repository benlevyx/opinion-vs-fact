import os
import json
import re
from urllib.parse import urlparse
from contextlib import contextmanager

from .config import data, apikey


def load_json_from_data(fname: str) -> dict:
    return json.load((data / fname).open('r'))


def regex_match(regex, text) -> bool:
    """Return True if the text matches the regex
    """
    return re.search(regex, text) is not None


def get_apikey() -> str:
    """Get my API keys (saved in project root)
    """
    with apikey.open('r') as f:
        key = f.read().strip('\n')
    return key


def parse_url(url: str) -> tuple:
    """Parse a URL string into domain and path.
    """
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '')
    path = parsed.path
    return domain, path


@contextmanager
def suppress_stream(stream):
    with open(os.devnull, "w") as devNull:
        orig = stream
        stream = devNull
        try:
            yield
        finally:
            stream = orig
