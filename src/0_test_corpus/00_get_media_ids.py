import pandas as pd

from opinion import config, api


mc = api.get_api_conn()
media = []
start, rows = 0, 100


if __name__ == '__main__':
    while True:
        data = mc.mediaList(start=start, rows=rows)
        if not data:
            break

        media.append(rows)
        start += rows

    df_media = pd.DataFrame(media)
    df_media = df_media[['media_id', 'name', 'url']]

    fout = 'all_media.csv'
    df_media.to_csv((config.data / fout))
