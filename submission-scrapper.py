import datetime
import json

import requests

from util import log, extend_dict, empty_directory_if_exists_then_create, remove_file_if_exists


def get_subreddits():
    subreddits_index_file = 'subreddits-index.json'

    with open(subreddits_index_file, 'r') as in_f:
        return json.load(in_f).get('subreddits')


def format_submission_dict(_submission: dict):
    keys = []
    # keys = ['active_user_count', 'allow_images', 'allow_videogifs', 'allow_videos', 'allowed_media_in_comments',
    #         'created_utc', 'description', 'display_name', 'display_name_prefixed', 'emojis_enabled', 'header_title',
    #         'id', 'lang', 'name', 'over18', 'primary_color', 'public_description', 'show_media', 'submission_type',
    #         'advertiser_category']

    final_dict = {}
    if len(keys) == 0:
        return _submission

    for key in keys:
        final_dict = extend_dict(final_dict, {key: _submission.get(key)})

    return final_dict


def save_submission(_save_directory: str, _submission: dict, _subreddit_name):
    with open(f'{_save_directory}/{_subreddit_name}/{_submission.get("name")}.json', 'w') as out_f:
        out_f.write(json.dumps(_submission, indent=4))


def save_to_index(_save_directory: str, _submissions: list, _subreddit_name: str):
    submissions_index_file = f'submissions-{_subreddit_name.lower()}-index.json'
    index_list = list()

    remove_file_if_exists(submissions_index_file)

    for _submission in _submissions:
        index_list.append({
            'name': _submission.get('name'),
            'title': _submission.get('title'),
            'created_utc': _submission.get('created_utc')
        })

        dt = datetime.datetime.now(datetime.timezone.utc)

        utc_time = dt.replace(tzinfo=datetime.timezone.utc)
        utc_timestamp = utc_time.timestamp()

        with open(f'{_save_directory}/{submissions_index_file}', 'w') as out_f:
            out_f.write(
                json.dumps({'subreddit': _subreddit_name, 'created_utc': utc_timestamp, 'size': len(_submissions),
                            'submissions': index_list},
                           indent=4))


def get_submissions_from_subreddit(_subreddit: dict, _save_directory: str):
    log(f'Getting submissions for {_subreddit}')
    start_time = datetime.datetime.now()

    after = None
    base_url = f'https://{_subreddit.get("url")}.json?limit=100'
    submissions = list()

    submission_path = f'{_save_directory}/{_subreddit.get("display_name")}'
    empty_directory_if_exists_then_create(submission_path)

    while True:
        url = f'{base_url}&after={after}' if after else base_url

        response = requests.get(url, headers={'User-Agent': 'bob'})
        res_body = response.json().get('data')
        submission_data_list = res_body.get('children')

        if len(submission_data_list) == 0:
            print()
            log(f'{_subreddit.get("display_name_prefixed")} | Finished')

            end_time = datetime.datetime.now()
            log(f'{_subreddit.get("display_name_prefixed")} | Fetching and saving {len(submissions)} submissions took '
                f'{(end_time - start_time).seconds} seconds')
            print()

            save_to_index(submission_path, submissions, _subreddit.get('display_name'))

            break

        for submission in [format_submission_dict(x.get('data')) for x in submission_data_list]:
            submissions.append(submission)
            save_submission(save_directory, submission, _subreddit.get('display_name'))
            after = submission.get('name')

        log(f'{_subreddit.get("display_name_prefixed")} | Fetched {len(submissions)} submissions')


if __name__ == '__main__':
    start = datetime.datetime.now()
    subreddit_limit = None
    save_directory = 'submissions'
    empty_directory_if_exists_then_create(save_directory)
    print()

    subreddits = get_subreddits()[:subreddit_limit] if subreddit_limit else get_subreddits()

    for subreddit in subreddits:
        get_submissions_from_subreddit(subreddit, save_directory)

    end = datetime.datetime.now()
    print()
    log(f'Fetching and saving submissions for {len(subreddits)} subreddits took {(end - start).seconds}')
