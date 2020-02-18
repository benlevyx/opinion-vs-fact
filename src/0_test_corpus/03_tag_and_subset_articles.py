import pandas as pd
from tqdm import tqdm

import opinion
from opinion import api, config


mc = api.get_api_conn()
MAX_OPINION = 25
MAX_NOT_OPINION = 25


def shuffle_data(df):
    return df.sample(frac=1)


def get_json_response(stories_id):
    return mc.story(stories_id)


def tag_story(json_response):
    model_output = opinion.is_opinion(json_response)
    return model_output


def sample_stories(df):
    df_shuffled = shuffle_data(df)
    opinion = []
    not_opinion = []

    pbar = tqdm(total=MAX_OPINION + MAX_NOT_OPINION)
    for stories_id in df_shuffled['stories_id']:
        json_response = get_json_response(stories_id)
        is_opinion = tag_story(json_response)[stories_id]['is_opinion']
        if is_opinion:
            if len(opinion) < MAX_OPINION:
                opinion.append(json_response)
                pbar.update()
        else:
            if len(not_opinion) < MAX_NOT_OPINION:
                not_opinion.append(json_response)
                pbar.update()
        if len(opinion) >= MAX_OPINION and len(not_opinion) >= MAX_NOT_OPINION:
            pbar.close()
            break
    all_stories = opinion + not_opinion
    return pd.DataFrame(all_stories)


def main():
    df_stories = pd.read_csv(config.data / 'stories.csv', index_col=0)
    sample_dfs = []
    for media_url in df_stories['media_url'].unique():
        print("Tagging stories from {}".format(media_url))

        res = sample_stories(df_stories.query('media_url == @media_url'))
        sample_dfs.append(res)
    df_samples = pd.concat(sample_dfs, axis=0)
    df_samples.to_csv(config.data / 'sampled_stories.csv', index=False)


if __name__ == '__main__':
    main()
