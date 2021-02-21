import argparse
from datetime import datetime
import snscrape.modules.twitter as twt
from typing import Callable

import writer

def parse_arguments():
    p = argparse.ArgumentParser()
    p.add_argument("-v", "--verbose", help="Toggle verbose output", action="store_true")
    p.add_argument("-s", "--start", help="Date to collect tweets from", type=str, default="now")
    p.add_argument("-e", "--end", help="Date to collect tweets until (only valid if using '--from'; must be earlier than the current time)", type=str)
    p.add_argument("-l", "--limit", help="Maximum number of tweets to scrape", type=int, default=5000)
    p.add_argument("-f", "--file", help="File to append tweets to. Will be created if doesn't already exist")
    p.add_argument("-o", "--output", help="Places the output in to <file>") 
    p.add_argument(
        "-t", "--terms",
        nargs="+",
        help="(Required) List of terms to use when searching twitter",
        required=True)

    return p.parse_args()

def scrape_tweets(*, start: str, end: str, num_tweets: int, terms: list[str]):
    scraper = twt.TwitterSearchScraper(
        " ".join(terms),
        " lang: en since:2021-01-12 until:2021-01-13 -filter:replies")
    
    csv_file = writer.CSVWriter(
        file_name=args.file,
        out_directory=args.output,
        row_names=["id", "date", "user", "url", "contents", "weight", "pos", "neu", "neg"])

    for i, tweet in enumerate(scraper.get_items()):
        if i > MAX_TWEETS:
            return

        csv_file.append([tweet.id, tweet.date, tweet.user, tweet.url, tweet.content])

def main():
    args = parse_arguments()
    
    # Test if date is valid
    # Test if MAX_TWEETS isnt negative
    # Print verbose stuff
    
    MAX_TWEETS = args.limit - 1
    SEARCH_TERMS = args.terms   

    scrape(
        start="",
        end="",
        num_tweets=MAX_TWEETS,
        terms=SEARCH_TERMS)    

if __name__ == "__main__":
    main()
