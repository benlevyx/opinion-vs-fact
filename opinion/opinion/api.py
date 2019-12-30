import mediacloud.api

from .utils import get_apikey


def get_api_conn(apikey=None):
    if not apikey:
        apikey = get_apikey()
    return mediacloud.api.AdminMediaCloud(apikey)
