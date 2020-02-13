import pandas as pd

from opinion import config, api


mc = api.get_api_conn()
media = []
start, rows = 0, 100


# if __name__ == '__main__':
#     print("Downloading all media ids.")
#     while True:
#         data = mc.mediaList(start=start, rows=rows)
#         if not data:
#             break

#         media.append(rows)
#         start += rows

#         # if start % 1000 == 0:
#         print("Downloaded {} media source ids.".format(start))

#     print("Done downloading ids.")

#     df_media = pd.DataFrame(media)
#     df_media = df_media[['media_id', 'name', 'url']]

#     print("Saving ids")
#     fout = 'all_media.csv'
#     df_media.to_csv((config.data / fout))
#     print("Done all tasks.")

if __name__ == '__main__':
    api.download_media_ids('all_media.csv')
