import feedparser
from config import FEEDS


def get_stories(feeds):
    for feed in feeds:
        for entry in feed['entries']:
            for story in entry['content']:
                yield story['value']

feeds = (feedparser.parse(url) for url in open(FEEDS).readlines())
stories = get_stories(feeds)
