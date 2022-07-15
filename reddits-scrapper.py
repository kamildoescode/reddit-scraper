import datetime
import json
from datetime import timezone

import requests

from util import extend_dict, log


def format_reddit_dict(_reddit: dict):
    reddit_base_url = 'reddit.com'
    keys = ['active_user_count', 'allow_images', 'allow_videogifs', 'allow_videos', 'allowed_media_in_comments',
            'created_utc', 'description', 'display_name', 'display_name_prefixed', 'emojis_enabled', 'header_title',
            'id', 'lang', 'name', 'over18', 'primary_color', 'public_description', 'show_media', 'submission_type',
            'advertiser_category']

    final_dict = {}
    for key in keys:
        final_dict = extend_dict(final_dict, {key: _reddit.get(key)})
        final_dict = extend_dict(final_dict, {'url': f'{reddit_base_url}/{_reddit.get("display_name_prefixed")}'})

    return final_dict


def save_reddit(_save_directory: str, _reddit: dict):
    with open(f'{_save_directory}/{_reddit.get("display_name")}.json', 'w') as out_f:
        out_f.write(json.dumps(reddit, indent=4))


def save_to_index(_save_directory: str, _reddits: list):
    index_list = list()

    for _reddit in _reddits:
        index_list.append({'display_name_prefixed': _reddit.get('display_name_prefixed'), 'name': _reddit.get('name'),
                           'url': _reddit.get('url')})

    dt = datetime.datetime.now(timezone.utc)

    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()

    with open('reddits-index.json', 'w') as out_f:
        out_f.write(
            json.dumps({'created_utc': utc_timestamp, 'size': len(_reddits), 'reddits': index_list}, indent=4))


if __name__ == '__main__':
    print()

    after = None
    base_url = 'https://www.reddit.com/reddits.json?limit=100'
    reddits = list()

    save_directory = 'reddits'

    start_time = datetime.datetime.now()

    while True:
        url = f'{base_url}&after={after}' if after else base_url

        response = requests.get(url, headers={'User-Agent': 'bob'})
        res_body = response.json().get('data')

        after = res_body.get('after')

        for reddit in [format_reddit_dict(x.get('data')) for x in res_body.get('children')]:
            reddits.append(reddit)
            save_reddit(save_directory, reddit)

        if not after:
            break

        log(f'Currently fetched and saved {len(reddits)} reddits')

    end_time = datetime.datetime.now()

    print()
    log(f'Fetching and saving {len(reddits)} took {end_time - start_time} seconds')

    save_to_index(save_directory, reddits)
