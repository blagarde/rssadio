import requests
from local_settings import MS_KEY
from urllib import quote_plus


BASE_QUERY = r'https://api.datamarket.azure.com/Bing/Search/v1/Composite?Sources=%%27News%%27&Query=%%27%s%%27&$format=json&$skip=%i'
STEP = 50


def get(query, skip=0):
    query = BASE_QUERY % (quote_plus(query), skip)
    print "Bing!", query
    jdct = requests.get(query, auth=(MS_KEY, MS_KEY)).json()
    return jdct['d']['results'][0]['News']


def xbinglinks(search, limit=100, forever=False, maxemptyqueries=2):
    skip = 0
    quota = maxemptyqueries
    while (forever or limit > 0) and quota > 0:
        quota -= 1
        results = get(search, skip=skip)
        for res in results:
            yield res['Description']
            limit -= 1
            quota = maxemptyqueries
            if limit <= 0 and not forever:
                raise StopIteration("Target number of links reached")
        skip += STEP