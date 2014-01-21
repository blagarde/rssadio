import re
from string import punctuation
from sklearn.feature_extraction.text import HashingVectorizer
from bing import xbinglinks


WHITESPACE_RE = re.compile('\s+', flags=re.UNICODE)
PUNCTUATION_RE = re.compile('[' + punctuation + '\s]+', flags=re.UNICODE)


def preprocess(doc):
    doc = PUNCTUATION_RE.sub(' ', doc)
    return WHITESPACE_RE.sub(' ', doc).strip(' ')


hv = HashingVectorizer()

X = []
y = []

topics = ['technology', 'sports']
for search_query in topics:
    y += [search_query]
    X += [preprocess(doc) for doc in xbinglinks(search_query, limit=10)]

hv.transform(X)