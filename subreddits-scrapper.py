import datetime
import json
from datetime import timezone

import requests

from util import extend_dict, log, remove_file_if_exists, empty_directory_if_exists_then_create


def format_subreddit_dict(_subreddit: dict):
    reddit_base_url = 'reddit.com'
    keys = []
    # keys = ['active_user_count', 'allow_images', 'allow_videogifs', 'allow_videos', 'allowed_media_in_comments',
    #         'created_utc', 'description', 'display_name', 'display_name_prefixed', 'emojis_enabled', 'header_title',
    #         'id', 'lang', 'name', 'over18', 'primary_color', 'public_description', 'show_media', 'submission_type',
    #         'advertiser_category']

    final_dict = {}
    if len(keys) == 0:
        return extend_dict(_subreddit, {'url': f'{reddit_base_url}/{_subreddit.get("display_name_prefixed")}'})

    for key in keys:
        final_dict = extend_dict(final_dict, {key: _subreddit.get(key)})
        final_dict = extend_dict(final_dict, {'url': f'{reddit_base_url}/{_subreddit.get("display_name_prefixed")}'})

    return final_dict


def save_subreddit(_save_directory: str, _subreddit: dict):
    with open(f'{_save_directory}/{_subreddit.get("display_name")}.json', 'w') as out_f:
        out_f.write(json.dumps(_subreddit, indent=4))


def save_to_index(_save_directory: str, _subreddits: list):
    subreddits_index_file = 'subreddits-index.json'
    index_list = list()

    remove_file_if_exists(subreddits_index_file)

    for _subreddit in _subreddits:
        index_list.append({
            'display_name': _subreddit.get('display_name'),
            'display_name_prefixed': _subreddit.get('display_name_prefixed'),
            'name': _subreddit.get('name'),
            'url': _subreddit.get('url'),
            'created_utc': _subreddit.get('created_utc')
        })

        dt = datetime.datetime.now(timezone.utc)

        utc_time = dt.replace(tzinfo=timezone.utc)
        utc_timestamp = utc_time.timestamp()

        with open(subreddits_index_file, 'w') as out_f:
            out_f.write(
                json.dumps({'created_utc': utc_timestamp, 'size': len(_subreddits), 'subreddits': index_list},
                           indent=4))


if __name__ == '__main__':
    print()

    after = None
    base_url = 'https://www.reddit.com/reddits.json?limit=100'
    subreddits = list()

    save_directory = 'subreddits'
    empty_directory_if_exists_then_create(save_directory)
    print()

    start_time = datetime.datetime.now()

    while True:
        url = f'{base_url}&after={after}' if after else base_url

        response = requests.get(url, headers={'User-Agent': 'bob'})
        res_body = response.json().get('data')

        after = res_body.get('after')

        for subreddit in [format_subreddit_dict(x.get('data')) for x in res_body.get('children')]:
            subreddits.append(subreddit)
            save_subreddit(save_directory, subreddit)

        if not after:
            break

        log(f'Currently fetched and saved {len(subreddits)} subreddits')

    save_to_index(save_directory, subreddits)
    print()
    end_time = datetime.datetime.now()
    log(f'Fetching and saving {len(subreddits)} subreddits took {(end_time - start_time).seconds} seconds')
