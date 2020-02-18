import pandas as pd

from opinion import config, utils


def transform_url(df):
    df['media_source'] = df['media_source'].apply(
        lambda x: x.replace('https', 'http')
    )
    return df


def process_url(url):
    try:
        domain, path = utils.parse_url(url)
        return domain
    except ValueError as e:
        print(e, url)
        return 'na'


def main():
    df_top50 = pd.read_csv(config.data / 'media_sources.csv')
    df_all = pd.read_csv(config.data / 'all_media.csv', index_col=0)

    df_all['url'] = df_all['url'].apply(process_url)
    df_top50['media_source'] = df_top50['media_source'].apply(process_url)

    df_merged = pd.merge(df_top50, df_all,
                         how='left',
                         left_on='media_source', right_on='url')
    df_merged = df_merged[['media_source', 'has_opinion', 'media_id', 'name']]
    df_merged.to_csv(config.data / 'media_with_ids.csv', index=False)


if __name__ == '__main__':
    main()
