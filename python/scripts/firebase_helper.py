#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 23:19:56 2020

@author: ma
"""

# TODO: find a way to batch update table

import firebase_admin as fb
import firebase_admin.db as fbdb
import pandas as pd


class Firebase(object):

    def __init__(self, file_creds):
        cred = fb.credentials.Certificate(file_creds)
        self.default_app = fb.initialize_app(cred)

    def update(url, sub_loc, d):
        loc = fbdb.reference(url=url)
        for sub in sub_loc:
            loc = loc.child(sub)
        loc.update(d)

    def set_df(df, url, sub_loc):
        loc = fbdb.reference(url=url)
        for sub in sub_loc:
            loc = loc.child(sub)
        df.apply(lambda row: loc.update({row.name: dict(row)}), axis=1)

    def get_df(url, sub_loc, return_df=True):
        loc = fbdb.reference(url=url)
        for sub in sub_loc:
            loc = loc.child(sub)
        res = loc.get()
        if return_df:
            res = [e for e in res if e is not None]
            res = pd.DataFrame(res)
        return res


#  def row_to_dict(row):
#      return {row.name: dict(row)}
#  db = fb.db.reference(url=URL)
#  items = db.child('items')
#  items.set({'temp3': {'question': 'a', 'answer': 'b'}})
#  items.update({'temp4': {'question': 'a', 'answer': 'b'}})
