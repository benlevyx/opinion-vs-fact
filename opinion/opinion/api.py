import requests

import pandas as pd
import mediacloud.api

from .config import data
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
        params = {'last_media_id': last_media_id, 'rows': rows, 'key': MY_KEY}
        print("last_media_id:{} rows:{}".format(last_media_id, rows))
        r = requests.get('https://api.mediacloud.org/api/v2/media/list', params=params, headers={'Accept': 'application/json'})
        resp = r.json()

        if len(resp) == 0:
            break

        last_media_id = resp[-1]['media_id']
        media.extend(resp)

    df_media = pd.DataFrame(media)
    df_media = df_media[['media_id', 'name', 'url']]

    print("Saving ids")
    df_media.to_csv((data / fout))
    media = []


def download_stories(media_id, start_date, end_date):
    start = 0
    rows = 100
    date_fmt_str = '%Y-%m-%dT%H:%M:%SZ'
    fq = 'publish_date:[{0} TO {1}]'.format(
            start_date.strftime(date_fmt_str),
            end_date.strftime(date_fmt_str)
        )
    collected_stories = []
    while True:
        params = {
            'last_processed_stories_id': start,
            'rows': rows,
            'q': 'media_id:{}'.format(media_id),
            'fq': fq,
            'key': MY_KEY
        }

        print("Fetching {} stories starting from {}".format( rows, start))
        r = requests.get( 'https://api.mediacloud.org/api/v2/stories/list/', params = params, headers = { 'Accept': 'application/json'} )
        stories = r.json()

        if len(stories) == 0:
            break

        start = stories[-1][ 'processed_stories_id' ]
        collected_stories.extend(stories)
    return collected_stories
