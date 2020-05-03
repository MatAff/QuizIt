
from random import random, randint
from functools import reduce
import numpy as np
import pandas as pd


class Learn(object):

    def get_recent_items(self, response_df, n):
        if response_df.shape[0] == 0:
            return []
        response_df = response_df.sort_values(by='ts', ascending=False)
        return response_df['key'][0:n]

    # TODO: refactor due to duplicate code in:
    # compute_item_mean, compute_item_mean_running, add_mu, add_w_mu
    def compute_item_mean(self, key, sorted_response_df):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        if len(item_responses.index) == 0 : return 0.0 # handle no data
        mu = item_responses.correct.mean()
        mu = np.round(mu, 5)
        return mu

    def compute_item_mean_running(self, key, sorted_response_df, r):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        if len(item_responses.index) == 0 : return 0.0 # handle no data
        resp_int = item_responses.correct.astype('int').values
        mu_r = reduce(lambda a, b: a * (1-r) + b * r, resp_int[::-1])
        return mu_r

    def order_retainer(self, s):
        small_addition = np.array(range(len(s), 0, -1)) / 10**6
        return s + small_addition
    
    def compute_item_count(self, key, sorted_response_df):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        return len(item_responses.index)
    
    def add_count(self, item_df, response_df):
        item_count = lambda k: self.compute_item_count(k, response_df)
        item_df['n'] = item_df.key.apply(item_count)
        return item_df

    def add_mu(self, item_df, response_df):
        item_mean = lambda k: self.compute_item_mean(k, response_df)
        item_df['mu'] = item_df.key.apply(item_mean)
        item_df['mu'] = self.order_retainer(item_df['mu'])
        return item_df

    def add_w_mu(self, item_df, response_df, r):
        run_mean = lambda k: self.compute_item_mean_running(k, response_df, r)
        item_df['mu_run'] = item_df.key.apply(run_mean)
        item_df['mu_run'] = self.order_retainer(item_df['mu_run'])
        return item_df

    def get_chunk(self, df, col, val, n, db=False):
        ser = df[col]
        ind = ser[ser==val].index[0]
        pos = df.index.get_loc(ind)
        start_pos = max(0, (pos - n))
        end_pos = (pos + n + 1)
        if db:
            print(pos, start_pos, end_pos)
        return df.iloc[start_pos:end_pos]

    def compute_near_mu(self, k, item_df, n):
        min_req_responses = 3
        chunk = self.get_chunk(item_df, 'key', k, n)
        chunk = chunk[chunk.n > 0]
        if len(chunk.index) < min_req_responses : return 0.0 
        return chunk.mu.mean()

    def add_near_mu(self, item_df, n):
        near_mu = lambda k: self.compute_near_mu(k, item_df, n)
        item_df['mu_near'] = item_df.key.apply(near_mu)
        item_df['mu_near'] = self.order_retainer(item_df['mu_near'])
        return item_df

    def simple(self, item_df, response_df):
        
        all_items = item_df

        # vary know threshold
        know_thresh = random() * 0.2 + 0.7 # 0.7-0.9
        print(f'current know threshold: {know_thresh}')

        # if reponses is empty return random item
        if response_df.shape[0] == 0:
            random_int = randint(0, 10)
            return item_df.iloc[random_int, :]

        # determine recent items
        recent_items = self.get_recent_items(response_df, n=5)
        item_df['recent'] = item_df.key.isin(recent_items)

        # compute current probabiliy
        response_df = response_df.sort_values(by='ts', ascending=False)

        # item count
        item_df = self.add_count(item_df, response_df)

        # simple mean
        item_df = self.add_mu(item_df, response_df)
        
        # discounted mean
        item_df = self.add_w_mu(item_df, response_df, r=0.75)

        # add near mu
        item_df = self.add_near_mu(item_df, 5)

        # combine
        item_df['prob'] = item_df['mu_run']
        item_df.loc[item_df.n == 0,'prob'] = item_df.loc[item_df.n ==0, 'mu_near']

        # sometime pick random known
        pick_known_prob = 0.15
        if random() < pick_known_prob:
            item_df = item_df[item_df.prob >= know_thresh]
            nr_items = len(item_df.index)
            if nr_items > 0:
                print('picking random known item')
                pos = randint(0, nr_items - 1)
                return item_df.iloc[pos, :]
        
        # pick item
        item_df = item_df[item_df.prob < know_thresh]
        item_df = item_df.sort_values('prob', ascending=False)
        item_df = item_df[(item_df.key.isin(recent_items))==False]
        item_row = item_df.iloc[0, :]

        # debug (print item around chosen item)
        print(item_row.key)
        chunk = self.get_chunk(all_items, 'key', item_row.key, 15)
        print(chunk)

        return item_row
