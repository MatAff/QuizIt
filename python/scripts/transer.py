#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 18 09:13:56 2020

@author: ma
"""

# TODO: save items under topic name
# TODO: update to accomodate multiple topics
# TODO: ensure entire sheet stores

from google_helper import Google
from firebase_helper import Firebase

# credentials
FILE_GS_CREDS = '../../../credentials/google_sheets_credentials.json'
FILE_GS_TOKEN = '../../../credentials/google_sheets_token.pickle'
FILE_FB_CREDS = '../../../credentials/' + \
                'quiz-it-c6643-firebase-adminsdk-32pqc-574194610f.json'
FB_URL = 'https://quiz-it-c6643.firebaseio.com'

# sheet details
SPANISH = {'id': '1LW69o3iJeJZUGCrJ1HfX19gMZXQNR0jGNbvscB6zQQA',
           'name': 'WordList'}
topic = 'spanish'


def main():

    # get sheet content
    gs = Google(FILE_GS_CREDS, FILE_GS_TOKEN)
    df = gs.sheet_content(SPANISH['id'], SPANISH['name'], 3)
    print(df.head(10))

    # add common key
    df.columns = ['question', 'answer', 'tag']
    df['key'] = df.iloc[:, 0] + "|" + df.iloc[:, 1]
    df = df[df.key.duplicated() == False]
    df = df.reset_index()
    print(df.head(10))

    # write to database
    try:
        Firebase(FILE_FB_CREDS)
    except Exception:
        pass
    Firebase.set_df(df, FB_URL, ['items', topic])


if __name__ == '__main__':
    main()
