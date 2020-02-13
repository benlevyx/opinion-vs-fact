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
    last_media_id = 0
    rows = 1000
    while True:
        params = { 'last_media_id': last_media_id, 'rows': rows, 'key': MY_KEY }
        print("last_media_id:{} rows:{}".format( last_media_id, rows))
        r = requests.get( 'https://api.mediacloud.org/api/v2/media/list', params = params, headers = { 'Accept': 'application/json'} )
        data = r.json()

        if len(data) == 0:
            break

        last_media_id = data[-1]['media_id']
        media.extend( data )

    fieldnames = [
        u'media_id',
        u'url',
        u'name'
    ]

    with open( '/tmp/media.csv', 'wb') as csvfile:
        print("open")
        cwriter = csv.DictWriter( csvfile, fieldnames, extrasaction='ignore')
        cwriter.writeheader()
        cwriter.writerows( media )
