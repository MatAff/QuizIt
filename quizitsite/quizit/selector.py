
import random
from functools import reduce
import numpy as np
import pandas as pd


class Selector(object):

    @staticmethod
    def random(items, responses, n=20):
        item_id = random.randint(0, n)
        return items[item_id]

    @staticmethod
    def responses_to_df(responses):
        resp_list = [r.to_dict() for r in responses]
        resp_df = pd.DataFrame(resp_list)
        return resp_df

    @staticmethod
    def items_to_df(items):
        item_list = [r.to_dict() for r in items]
        item_df = pd.DataFrame(item_list)
        return item_df

    @staticmethod
    def get_recent_items(response_df, n):
        response_df = response_df.sort_values(by='ts', ascending=False)
        return response_df['key'][0:n]

    @staticmethod
    def compute_item_mean(key, sorted_response_df):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        mu = item_responses.correct.mean()
        if np.isnan(mu) : mu = 0.0  # handle no data
        mu = np.round(mu, 5)
        return mu

    @staticmethod
    def compute_item_mean_running(key, sorted_response_df, r=0.75):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        resp_int = item_responses.correct.astype('int').values
        mu_r = reduce(lambda a, b: a * (1-r) + b * r, resp_int[::-1], 0)
        return mu_r

    @staticmethod
    def order_retainer(s):
        small_addition = np.array(range(len(s), 0, -1)) / 10**6
        return s + small_addition

    @staticmethod
    def simple(items, responses):
        
        know_thresh = 0.8

        # convert responses to df
        response_df = Selector.responses_to_df(responses)

        # convert items to df
        item_df = Selector.items_to_df(items)

        # determine recent items
        recent_items = Selector.get_recent_items(response_df, n=5)
        item_df['recent'] = item_df.key.isin(recent_items)

        # compute current probabiliy
        response_df = response_df.sort_values(by='ts', ascending=False)
        print(response_df)

        # simple mean
        item_mean = lambda k: Selector.compute_item_mean(k, response_df)
        item_df['mu'] = item_df.key.apply(item_mean)
        item_df['mu'] = Selector.order_retainer(item_df['mu'])

        # discounted mean
        run_mean = lambda k: Selector.compute_item_mean_running(k, response_df)
        item_df['mu_run'] = item_df.key.apply(run_mean)
        item_df['mu_run'] = Selector.order_retainer(item_df['mu_run'])

        # debug
        # print(item_df[['key', 'recent', 'mu_run']].head(30))   

        # pick item\
        item_df = item_df[item_df.mu_run < know_thresh]
        item_df = item_df.sort_values('mu_run', ascending=False)
        item_df = item_df[(item_df.key.isin(recent_items))==False]
        item_key = item_df.key.iloc[0]

        return item_key

