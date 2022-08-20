from json import dumps as json_dumps

from requests import get, Response

import util
from util import get_random_user_agent, extend_dict, empty_directory_if_exists_then_create, remove_file_if_exists, info

REDDIT_BASE_URL = 'https://www.reddit.com/reddits.json?limit=100'
SUBREDDIT_SAVE_PATH = 'subreddits'
SUBREDDIT_INDEX_FILE_NAME = 'subreddits-index.json'


class SubredditScraper:
    def __init__(self, limit: int | None):
        """
        Subreddit Scraper
        @param limit: How many subreddits to scrape, can be None to scrape all
        """

        self.limit = limit

    def scrape(self, save: bool, index: bool, detail_log: bool) -> list[dict]:
        """
        Scrape the subreddits
        @param save: Save subreddit data to a json file
        @param index: Save subreddit index data
        @param detail_log: Include detailed logs
        @return: list of json objects representing each individual subreddit
        """

        def __finish_scraping() -> list[dict]:
            """
            Wrapped method for everything that needs to take place when scraping is finished
            @return: list of subreddits
            """

            self._log_fetched(save, len(subreddits))
            if index:
                SubredditScraper._save_to_index(subreddits)

            return subreddits

        subreddits: list[dict]
        subreddits = list()

        after: str | None
        after = None

        if save:
            empty_directory_if_exists_then_create(SUBREDDIT_SAVE_PATH)

        while True:
            url: str
            url = f'{REDDIT_BASE_URL}?limit=100&after={after}' if after else REDDIT_BASE_URL

            response: Response
            response = get(url, headers={'User-Agent': get_random_user_agent()})

            res_body: dict
            res_body = response.json().get('data')

            after = res_body.get('after')

            for subreddit in \
                    [SubredditScraper._format_subreddit_dict(x.get('data')) for x in res_body['children']]:
                if len(subreddits) >= self.limit:
                    return __finish_scraping()

                subreddits.append(subreddit)
                if detail_log:
                    self._log_fetched(save, len(subreddits))

                if save:
                    SubredditScraper._save_subreddit(subreddit)

                if len(subreddits) == self.limit:
                    return __finish_scraping()

            if not after:
                break

        return __finish_scraping()

    def _log_fetched(self, _save: bool, _size: int) -> None:
        """Wrapper method for detailed log"""
        info(f'Fetched {"and saved " if _save else ""}{_size} subreddits / limit: {self.limit}')

    @staticmethod
    def _save_subreddit(_subreddit: dict):
        with open(f'{SUBREDDIT_SAVE_PATH}/{_subreddit.get("display_name")}.json', 'w') as out_f:
            out_f.write(json_dumps(_subreddit, indent=4))

    @staticmethod
    def _format_subreddit_dict(_subreddit: dict) -> dict:
        """
        Format subreddit data
        @return: Formatted subreddit data
        """
        reddit_base_url = 'reddit.com'

        return extend_dict(_subreddit, {'url': f'{reddit_base_url}/{_subreddit.get("display_name_prefixed")}'})

    @staticmethod
    def _save_to_index(_subreddits: list[dict]) -> None:
        index_list: list[dict]
        index_list = list()

        remove_file_if_exists(SUBREDDIT_INDEX_FILE_NAME)

        for _subreddit in _subreddits:
            index_list.append({
                'display_name': _subreddit.get('display_name'),
                'display_name_prefixed': _subreddit.get('display_name_prefixed'),
                'name': _subreddit.get('name'),
                'url': _subreddit.get('url'),
                'created_utc': _subreddit.get('created_utc')
            })

            utc_timestamp = util.get_current_timestamp_utc()

            with open(f'{SUBREDDIT_SAVE_PATH}/{SUBREDDIT_INDEX_FILE_NAME}', 'w') as out_f:
                out_f.write(
                    json_dumps({'created_utc': utc_timestamp, 'size': len(_subreddits), 'subreddits': index_list},
                               indent=4))
