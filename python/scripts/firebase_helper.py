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


    def set_df(df, url, table_name):
        db = fbdb.reference(url=url)
        table = db.child(table_name)
        df.apply(lambda row: table.update({row.name: dict(row)}), axis=1)


    def get_df(url, table_name):
        db = fbdb.reference(url=url)
        table = db.child(table_name)
        l = table.get()
        l = [e for e in l if e is not None]
        return pd.DataFrame(l)


#def row_to_dict(row):
#    return {row.name: dict(row)}

#db = fb.db.reference(url=URL)
#items = db.child('items')

#items.set({'temp3': {'question': 'a', 'answer': 'b'}})
#items.update({'temp4': {'question': 'a', 'answer': 'b'}})

