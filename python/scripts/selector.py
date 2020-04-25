#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 11:09:08 2020

@author: ma
"""

# TODO: figure out why words keep repeating >> Done
# TODO: implement weighted method to estimate probability >> Done
# TODO: implement method to avoid close repetition of items >> Done
# TODO: create more efficient method to select next item
# TODO: clean up
# TODO: condider keeping track of learn items, rather than pick every time

import numpy as np
import pandas as pd


class Selector(object):

    def __init__(self, items):
        self.items = items
        self.recent = []

    def check_recent(self, item):
        if item.key in self.recent:
            return False
        else:
            self.recent.append(item.key)
            if len(self.recent) > 5:
                self.recent.pop(0)
            return True

    def mean_resp(self, k, responses):
        sub_res = responses[responses.key == k]
        values = sub_res.correct.astype('int').values
        mu = np.append(values, self.basic_prob.loc[k, 'prob']).mean()
        return mu

    def mean_w_resp(self, k, responses):
        sub_res = responses[responses.key == k]
        values = sub_res.correct.astype('int').values
        # print(values)
        mu = self.basic_prob.loc[k, 'prob']
        for v in values:
            mu = 0.1 * mu + 0.9 * v
        # print(round(mu, 2))
        return mu

    def update_basic_prob(self, responses):
        prior = np.repeat(0.5, self.items.shape[0])
        self.basic_prob = pd.DataFrame(prior, index=self.items.key,
                                       columns=['prob'])
        keys = responses.key.unique()
        keys = keys[pd.Series(keys).apply(lambda k: k in self.items.key.values)]
        for k in keys:
            # self.basic_prob.loc[k, 'prob'] = self.mean_resp(k, responses)
            self.basic_prob.loc[k, 'prob'] = self.mean_w_resp(k, responses)
        # print(self.basic_prob.head(20))

    def select_random(self):
        return self.items.sample(1).iloc[0, :]

    def select_basic_prob(self):
        # print(self.items.head(10))
        learn_items = self.items[(self.basic_prob.values < 0.8)]
        # print(learn_items.head(10))
        item_nr = np.random.randint(0, 10, 1)[0]
        return learn_items.iloc[item_nr, :]

    def select(self, responses=None, method='random'):
        if method == 'random':
            return self.select_random()
        if method == 'basic_prob':
            self.update_basic_prob(responses)
            non_recent = False
            while non_recent == False:
                item = self.select_basic_prob()
                non_recent = self.check_recent(item)
            # print(self.basic_prob.loc[item.key])
            print('\nwords learned: ' +
                  str((self.basic_prob.values >= 0.8).sum()))
            return item
