from random import random, randint
from functools import reduce
import numpy as np
import pandas as pd
import re

from quizit.text_comparison import TextComparison
from quizit.format import Format


def split_by_pipe(t):
        return t.split('|')

def replace_at(t):
    return [t.replace('@', l) for l in ['o', 'a']]

def handle_paren(t):
    in_paren = re.search(r'\((.*?)\)',t)
    if in_paren is None:
        return t
    in_paren = in_paren.group(1)
    with_paren = f'({in_paren})'
    options = in_paren.split('/')
    if len(options) == 1:
        options.append('')
    with_options =  [t.replace(with_paren, opt) for opt in options]
    return [t.replace('  ', ' ') for t in with_options]

def handle_string(t):
    if '|' in t:
        return split_by_pipe(t)
    elif '@' in t:
        return replace_at(t)
    elif '(' in t:
        return handle_paren(t)
    else:
        return [t]

def expand_options(answer_list):
    res_list = []
    for e in answer_list:
        res = handle_string(e)
        if (len(res)) > 1 or (res[0] != e):
            res = expand_options(res)
        res_list.extend(res)     
    return res_list   

class Learn(object):

    know_thresh_low = 0.7
    know_thresh_high = 0.9
    recent_n = 5
    run_discount = 0.75
    pick_known_prob = 0.15

    def get_recent_items(self, sorted_response_df, n):
        n = min(len(sorted_response_df.index), n)
        recent_items = sorted_response_df['key'][0:n]
        return recent_items

    def order_retainer(self, s):
        small_addition = np.array(range(len(s), 0, -1)) / 10**6
        return s + small_addition

    def get_chunk(self, df, col, val, n):
        ser = df[col]
        ind = ser[ser==val].index[0]
        pos = df.index.get_loc(ind)
        start_pos = max(0, (pos - n))
        end_pos = (pos + n + 1)
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

    def compute_item_stats(self, key, sorted_response_df, r):
        item_responses = sorted_response_df[sorted_response_df.key==key]
        n = len(item_responses.index)
        if n == 0 : 
            mu = 0.0
            mu_run = 0.0
            return {'n':n, 'mu': mu, 'mu_run': mu_run}
        mu = np.round(item_responses.correct.mean(), 5)        
        resp = item_responses.correct.astype('int').values
        mu_run = reduce(lambda a, b: a * (1-r) + b * r, resp[::-1])
        return {'n':n, 'mu': mu, 'mu_run': mu_run}

    def add_item_stats(self, item_df, response_df):

        # sort responses
        response_df = response_df.sort_values(by='ts', ascending=False)
        
        # determine recent items
        recent_items = self.get_recent_items(response_df, n=self.recent_n)
        item_df['recent'] = item_df.key.isin(recent_items)

        # compute items stats
        r = self.run_discount
        get_item_stats = lambda k: self.compute_item_stats(k, response_df, r)
        item_stats = item_df.key.apply(get_item_stats)
        item_stats_df = item_stats.apply(pd.Series)
        item_df = pd.concat([item_df, item_stats_df], axis=1)
        item_df['mu'] = self.order_retainer(item_df['mu'])
        item_df['mu_run'] = self.order_retainer(item_df['mu_run'])

        # compute near stats
        item_df = self.add_near_mu(item_df, 5)

        # combine
        item_df['prob'] = item_df['mu_run']
        fill = item_df.n == 0
        item_df.loc[fill,'prob'] = item_df.loc[fill, 'mu_near']

        # word score
        word_score = item_df.prob.sum()
        print(f'word score: {word_score}')
        
        return item_df, word_score

    def get_know_thresh(self, verbose=False):
        rand_range = lambda low, high: random() * (high - low) + low
        know_thresh = rand_range(self.know_thresh_low, self.know_thresh_high)
        if verbose:
            print(f'current know threshold: {know_thresh}')
        return know_thresh

    def simple_n(self, item_df, response_df, n, exclude=None):
        
        know_thresh = self.get_know_thresh(True)
        
        # if reponses is small return random items
        if response_df.shape[0] < n:
            rows = np.randint(0, 2 * n, n)
            return item_df.iloc[rows, :]

        # add item statistics
        item_df, word_score = self.add_item_stats(item_df, response_df)

        # mark exclude as recent
        if exclude is not None:
            item_df.loc[item_df.key.isin(exclude), 'recent'] = True

        # retain known items
        known_items = item_df[item_df.prob >= know_thresh]
                
        # pick item
        item_df = item_df[item_df.prob < know_thresh]
        item_df = item_df[item_df.recent==False]
        picked_items = item_df.iloc[0:n, :]

        if known_items.shape[0] > 10:
            for r in range(picked_items.shape[0]):
                if random() < self.pick_known_prob:
                    print('picking random known item')
                    pos = randint(0, known_items.shape[0] - 1)
                    picked_items.iloc[r, :] = known_items.iloc[pos, :]

        return picked_items, word_score

    def compare_text(self, given, correct):
        tc = TextComparison(given, correct)
        change_count = tc.dist()
        if change_count < 5:
            change_str = tc.change()
            change_str = 'Changes: ' + change_str
            return change_str
        return ''

    def create_feedback(self, correct, item, answer):
        # TODO: move this in the learn as this is not DJ specific
        
        if correct:
            feedback = 'Correct: ' + item.question + ' = ' + item.answer
        else:
            change_str = self.compare_text(answer, item.answer)
            feedback = 'Nope: ' + item.question + ' = ' + item.answer
            feedback += '\nYou said: ' + answer
            feedback += '\n' + change_str
        return feedback

    # def at_to_alt(self, answer, alts):
    #     if '@' in answer:
    #         add = [answer.replace('@', l) for l in ['o', 'a']]
    #         if len(alts) > 0:
    #             alts = '|'.join([alts, *add])
    #         else:
    #             alts = '|'.join(add)
    #     return alts

    def check(self, item, given_answer, answer, alts):

        # handle punctuation
        given_answer = Format.add_accents(given_answer)
        given_answer = Format.remove(given_answer, accents=False)
        answer = Format.remove(answer, accents=False)
        alts = Format.remove(alts, accents=False)
        alts = alts.replace('^nan', '') # remove accidentally introduced nan

        # add answer variations
        answer_options = expand_options([answer, alts])

        # check answer against correct answers
        correct = False
        for opt in answer_options:
            if given_answer == opt:
                correct = True
                break
        
        # create feedback
        # TODO: create feedback using closest match
        feedback = self.create_feedback(correct, item, given_answer)

        return correct, feedback

