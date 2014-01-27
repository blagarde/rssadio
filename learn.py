import os
import re
import numpy as np
from string import punctuation
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn import linear_model
from feeds import stories
from cPickle import load, dump
from config import MODEL, GOOD, BAD


WHITESPACE_RE = re.compile('\s+', flags=re.UNICODE)
PUNCTUATION_RE = re.compile('[' + punctuation + '\s]+', flags=re.UNICODE)


def preprocess(doc):
    doc = PUNCTUATION_RE.sub(' ', doc)
    return WHITESPACE_RE.sub(' ', doc).strip(' ')


class App(object):
    def __init__(self):
        self.hv = HashingVectorizer(norm=None, non_negative=True)
        if os.path.isfile(MODEL):
            self.clf = load(MODEL)
        else:
            self.clf = linear_model.SGDClassifier(warm_start=True)
            zeros = self.vector('seed')
            self.clf.partial_fit(zeros, np.unique([GOOD]), classes=(GOOD, BAD))

    def feed(self):
        for doc in stories:
            self.pred_X = self.vector(doc)
            self.pred_y = self.clf.predict(self.pred_X)
            if self.pred_y == GOOD:
                yield doc

    def save_model(self):
        dump(self.clf, MODEL)

    def train(self, doc, y):
        X = self.vector(doc)
        self.clf.partial_fit(X, [y], classes=(GOOD, BAD))

    def vector(self, doc):
        clean = preprocess(doc)
        return self.hv.transform([clean])

    def score(self, y):
        print self.clf.score(self.pred_X, [y])


if __name__ == "__main__":
    app = App()
    for doc in app.feed():
        print doc
        label_dct = {'G': GOOD, 'B': BAD, 'S': 'skip'}
        value = ''
        while value.upper() not in label_dct:
            value = raw_input("What do you think about the above?\n(G)ood | (B)ad | (S)kip\n").upper()
        if value == 'S':
            continue
        label = label_dct[value]
        app.score(label)
        app.train(doc, label)
