from SubredditScraper import SubredditScraper
from util import log, warn


def scrape_subreddits():
    limit: int | None
    limit = None
    while limit is None:
        inp = input('Subreddit limit: ')
        try:
            limit = int(inp)
        except:
            pass

    scraper: SubredditScraper
    scraper = SubredditScraper(limit=None if limit == 0 else limit)

    """Should export subreddit data"""
    save: bool | None
    save = None
    while save is None:
        inp = input('Save fetched data? [1/0]: ')
        save = True if inp == '1' else False if inp == '0' else None

    """Should export subreddit index data"""
    index: bool | None
    index = None
    while index is None:
        inp = input('Save index data? [1/0]: ')
        index = True if inp == '1' else False if inp == '0' else None

    """Should include detailed log"""
    detail_log: bool | None
    detail_log = None
    while detail_log is None:
        inp = input('More detailed log? [1/0]: ')
        detail_log = True if inp == '1' else False if inp == '0' else None

    scraper.scrape(save=save, index=index, detail_log=detail_log)


if __name__ == '__main__':
    print('What would you want to scrape: ')
    print('\t1. subreddits')
    # print('\t2. submissions')
    print('\t0. exit')

    while True:
        print()
        choice = input('Choice : ')

        if choice == '0':
            break
        elif choice == '1':
            log('Scraping subreddits')
            scrape_subreddits()
            break
        # elif choice == '2':
        #     log('Scraping submissions')
        #     break
        else:
            warn('Incorrect input')
