from datetime import date, timedelta

import pandas as pd

from opinion import config, api


START_DATE = date(2020, 1, 1)
END_DATE = date(2020, 2, 1)
fout = config.data / 'stories.csv'


mc = api.get_api_conn()


def filter_sources(df):
    df_filtered = df.query('has_opinion == "yes" & keep == 1')
    df_filtered = df_filtered.drop_duplicates('media_source')
    return df_filtered


def download_stories_single_source(media_id):
    q = 'media_id:{}'.format(int(media_id))
    date_fmt_str = '%Y-%m-%dT%H:%M:%SZ'
    fq = 'publish_date:[{0} TO {1}]'.format(
            START_DATE.strftime(date_fmt_str),
            END_DATE.strftime(date_fmt_str)
        )
    print(q)
    print(fq)
    stories = []
    last_id = 0
    while True:
        print("last processed story id:{}".format(last_id))
        resp = mc.storyList(solr_query=q, solr_filter=fq,
                            last_processed_stories_id=last_id)
        if len(resp) == 0:
            break
        stories.extend(resp)
        last_id = resp[-1]['processed_stories_id']
    df = pd.DataFrame(stories)
    return df


# def download_stories_single_source(media_id, sample=1000):
#     stories = api.download_stories(media_id, START_DATE, END_DATE)
#     res = pd.DataFrame(stories)
#     if sample:
#         res = res.sample(n=sample)
#     return res


def download_all_stories(df):
    dfs = []
    print(df.columns)
    for mid, mname in zip(df['media_id'], df['name']):
        print("Downloading media source {0}, id:{1}".format(mname, mid))
        dfs.append(download_stories_single_source(mid))
    df_stories = pd.concat(dfs, axis=0, sort=False)
    return df_stories


def main():
    media_sources = pd.read_csv(config.data / 'media_with_ids_keepcol.csv')

    media_sources = filter_sources(media_sources)
    media_sources['media_id'] = media_sources['media_id'].apply(int)
    df_stories = download_all_stories(media_sources)
    df_stories.to_csv(fout)


if __name__ == '__main__':
    main()
