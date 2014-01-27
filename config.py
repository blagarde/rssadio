import os


HERE = os.path.abspath(os.path.dirname(__file__))
FEEDS = os.path.join(HERE, 'feeds.txt')
MODEL = os.path.join(HERE, 'model.pkl')
GOOD, BAD = 'GOOD', 'BAD'
