import csv
import requests

import mediacloud.api

from .utils import get_apikey


MY_KEY = get_apikey()


def get_api_conn(apikey=None):
    if not apikey:
        apikey = get_apikey()
    return mediacloud.api.AdminMediaCloud(apikey)


def download_media_ids(fout: str):
    media = []
    start = 0
    rows = 100
    while True:
        params = { 'start': start, 'rows': rows, 'key': MY_KEY }
        print("start:{} rows:{}".format( start, rows))
        r = requests.get( 'https://api.mediacloud.org/api/v2/media/list', params = params, headers = { 'Accept': 'application/json'} )
        data = r.json()

        if len(data) == 0:
            break

        start += rows
        media.extend(data)

    fieldnames = [
        u'media_id',
        u'url',
        u'name'
    ]

    with open((data / fout), 'wb') as csvfile:
        print("open")
        cwriter = csv.DictWriter( csvfile, fieldnames, extrasaction='ignore')
        cwriter.writeheader()
        cwriter.writerows( media )
