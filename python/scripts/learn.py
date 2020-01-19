#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 12:27:33 2020

@author: ma
"""

# TODO: find way to check if Firebase app exists
# TODO: consider implementing Learn as a generator

import time
import datetime
import pandas as pd
from firebase_helper import Firebase

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

class ItemSelector(object):
    
    def __init__(self, items):
        self.items = items

    def estimate_prob(self, responses):
        prob = pd.DataFrame(0.5, index = items.key)
    def select(responses):
        

class Learn(object):

    def __init__(self, topic, user):
        self.topic = topic
        self.user = user
        self.user_loc = user.replace('@', '__at__',).replace('.', '__dot__')
        self.items = get_items_fb(['items', topic])
        self.resp_sub_loc = ['response', topic, self.user_loc]
        res = Firebase.get_df(FB_URL, self.resp_sub_loc, False)
        self.responses = pd.DataFrame.from_dict(res, orient='index')

    def pick(self):
        return self.items.sample(1).iloc[0, :]

    def evalute(self, item, response):
        correct = item.answer == response
        ts = time.time()
        ts_str = datetime.datetime.now().replace(microsecond=0).isoformat()
        store = {ts_str: {'ts': ts, 'key': item.key, 'correct': correct}}
        Firebase.update(FB_URL, self.resp_sub_loc, store)
        pd.concat([learn.responses, pd.DataFrame(store).T]) # update local info

    def next(self):
        item = self.pick()
        response = input(item.question + ': ')
        if response == item.answer:
            print("correct")
        else:
            print("incorrect")
        self.evalute(item, response)


def main():

    learn = Learn(TOPIC, USER)

    running = True
    while running:
        learn.next()


if __name__ == '__main__':
    main()
