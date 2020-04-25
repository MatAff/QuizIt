#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:27:33 2020

@author: ma
"""

# TODO: find way to check if Firebase app exists
# TODO: consider implementing Learn as a generator
# TODO: use current approach
# TODO: enable system commen like EXIT, FLAG

import time
import datetime
import pandas as pd
from firebase_helper import Firebase
from selector import Selector

FILE_FB_CREDS = '../../../credentials/' + \
                'quiz-it-c6643-firebase-adminsdk-32pqc-574194610f.json'
FB_URL = 'https://quiz-it-c6643.firebaseio.com'
TOPIC = 'spanish'
USER = 'mathijsaffourtit@gmail.com'


def get_items_fb(sub_loc):
    try:
        Firebase(FILE_FB_CREDS)
    except Exception:
        pass
    return Firebase.get_df(FB_URL, sub_loc)


def remove_accents(t):
    acc = 'âäàåáêëèéïîìíóüçúûùññ'
    rep = 'aaaaaeeeeiiiioucuuunn'
    for e in zip(acc, rep):
        t = t.replace(e[0], e[1])
    #  from string import maketrans
    return t


def remove_punc(t):
    punc = '?!,.()'
    for e in punc:
        t = t.replace(e[0], "")
    return t


def remove(t, punc=True, accents=True):
    if punc:
        t = remove_punc(t)
    if accents:
        t = remove_accents(t)
    return t


class Learn(object):

    def __init__(self, topic, user):
        self.topic = topic
        self.user = user
        self.user_loc = user.replace('@', '__at__',).replace('.', '__dot__')
        self.items = get_items_fb(['items', topic])
        self.resp_sub_loc = ['response', topic, self.user_loc]
        res = Firebase.get_df(FB_URL, self.resp_sub_loc, False)
        self.responses = pd.DataFrame.from_dict(res, orient='index')
        self.item_selector = Selector(self.items)

    def evalute(self, item, response):
        correct = remove(item.answer) == remove(response)
        ts = time.time()
        ts_str = datetime.datetime.now().replace(microsecond=0).isoformat()
        store = {ts_str: {'ts': ts, 'key': item.key, 'correct': correct}}
        Firebase.update(FB_URL, self.resp_sub_loc, store)
        self.responses = pd.concat([self.responses, pd.DataFrame(store).T])
        return correct

    def next(self):
        item = self.item_selector.select(self.responses, method='basic_prob')
        response = input('\n' + item.question + ': ')
        correct = self.evalute(item, response)
        if correct:
            print("correct")
        else:
            print("incorrect: " + item.answer)


def main():

    learn = Learn(TOPIC, USER)

    running = True
    while running:
        learn.next()


if __name__ == '__main__':
    main()
