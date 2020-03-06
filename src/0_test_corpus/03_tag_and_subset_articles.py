import pandas as pd
import sys
# from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError

import opinion
from opinion import api, config, utils, timeout


mc = api.get_api_conn()
MAX_OPINION = 10
MAX_NOT_OPINION = 20


def trim_urls(df):
    df['media_url'] = df['media_url'].apply(lambda x: utils.parse_url(x)[0])
    return df


def shuffle_data(df):
    return df.sample(frac=1)


def get_json_response(stories_id):
    return mc.story(stories_id, text=True)


def tag_story(json_response):
    model_output = opinion.is_opinion(json_response)
    return model_output


def sample_stories(df, media_url):
    df_shuffled = shuffle_data(df)
    opinion = []
    not_opinion = []

    n_total = len(df_shuffled['stories_id'])
    n_timeouts = 0
    for i, stories_id in enumerate(df_shuffled['stories_id']):
        try:
            with timeout.timeout(seconds=1):
                with utils.suppress_stream(sys.stderr):
                    json_response = get_json_response(stories_id)
            is_opinion = tag_story(json_response)[stories_id]['is_opinion']
            if is_opinion:
                if len(opinion) < MAX_OPINION:
                    opinion.append(json_response)
            else:
                if len(not_opinion) < MAX_NOT_OPINION:
                    not_opinion.append(json_response)
        except (TimeoutError, ConnectionError) as e:
            print(e)
            n_timeouts += 1
        finally:
            sys.stdout.write("\r{7} -- Checked {0}/{1} stories -- {2}/{3} opinion -- {4}/{5} not opinion -- {6} timeouts".format(
                    i, n_total,
                    len(opinion), MAX_OPINION,
                    len(not_opinion), MAX_NOT_OPINION,
                    n_timeouts,
                    media_url
                ))
            sys.stdout.flush()

            if len(opinion) >= MAX_OPINION and len(not_opinion) >= MAX_NOT_OPINION:
                break
    print('\r')
    all_stories = opinion + not_opinion
    return pd.DataFrame(all_stories)


def main():
    print("loading data")
    df_stories = pd.read_csv(config.data / 'stories.csv', index_col=0)
    df_stories = trim_urls(df_stories)
    sample_dfs = []
    for media_url in df_stories['media_url'].unique():
        # For some reason, CNN is impossible to find opinion articles with
        # Likely because all the CNN articles are via RSS
        if media_url == "cnn.com":
            continue
        print("Tagging stories from {}".format(media_url))

        res = sample_stories(df_stories.query('media_url == @media_url'), media_url)
        sample_dfs.append(res)
    df_samples = pd.concat(sample_dfs, axis=0)
    df_samples.to_csv(config.data / 'sampled_stories.csv', index=False)


if __name__ == '__main__':
    main()
