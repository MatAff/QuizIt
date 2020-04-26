
import random
from functools import reduce
import numpy as np
import pandas as pd


class Learn(object):

    def get_recent_items(self, response_df, n):
        if response_df.shape[0] == 0:
            return []
        response_df = response_df.sort_values(by='ts', ascending=False)
        return response_df['key'][0:n]

    def compute_item_mean(self, key, sorted_response_df):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        mu = item_responses.correct.mean()
        if np.isnan(mu) : mu = 0.0  # handle no data
        mu = np.round(mu, 5)
        return mu

    def compute_item_mean_running(self, key, sorted_response_df, r=0.75):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        resp_int = item_responses.correct.astype('int').values
        mu_r = reduce(lambda a, b: a * (1-r) + b * r, resp_int[::-1], 0)
        return mu_r

    def order_retainer(self, s):
        small_addition = np.array(range(len(s), 0, -1)) / 10**6
        return s + small_addition

    def simple(self, item_df, response_df):
        
        know_thresh = 0.8

        # if reponses is empty return random item
        if response_df.shape[0] == 0:
            rand_int = random.randint(0, 10)
            return item_df.iloc[rand_int, :]

        # determine recent items
        recent_items = self.get_recent_items(response_df, n=5)
        item_df['recent'] = item_df.key.isin(recent_items)

        # compute current probabiliy
        response_df = response_df.sort_values(by='ts', ascending=False)
        print(response_df)

        # simple mean
        item_mean = lambda k: self.compute_item_mean(k, response_df)
        item_df['mu'] = item_df.key.apply(item_mean)
        item_df['mu'] = self.order_retainer(item_df['mu'])

        # discounted mean
        run_mean = lambda k: self.compute_item_mean_running(k, response_df)
        item_df['mu_run'] = item_df.key.apply(run_mean)
        item_df['mu_run'] = self.order_retainer(item_df['mu_run'])
        # print(item_df[['key', 'recent', 'mu_run']].head(30)) # debug

        # pick item
        item_df = item_df[item_df.mu_run < know_thresh]
        item_df = item_df.sort_values('mu_run', ascending=False)
        item_df = item_df[(item_df.key.isin(recent_items))==False]
        item_row = item_df.iloc[0, :]
        print(item_row)

        return item_row

