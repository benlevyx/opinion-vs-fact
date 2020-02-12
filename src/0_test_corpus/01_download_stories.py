from datetime import date, timedelta

import pandas as pd

from opinion import config, utils, api


START_DATE = date(2020, 1, 1)
END_DATE = date(2020, 2, 1)


mc = api.get_api_conn()
media_sources = pd.read_csv(config.data / 'media_sources.csv')


def filter_sources(df):
    return df.query('has_opinion == "yes"')


def download_stories_single_source(api, media_source):
    pass