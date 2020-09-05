#!/usr/bin/env python3

# Note: run instructions
# python3 manage.py shell
# import transfer

import os

from quizit.models import Item
from google_helper import Google

# credentials
base_path = '../../../credentials'
if os.path.exists(base_path) == False:
    base_path = '/home/bitnami/creds/'
FILE_GS_CREDS = os.path.join(base_path, 'google_sheets_credentials_secondary.json')
FILE_GS_TOKEN = os.path.join(base_path, 'google_sheets_token_secondary.pickle')

# verify credentials exist
assert os.path.exists(FILE_GS_CREDS), FILE_GS_CREDS
assert os.path.exists(FILE_GS_TOKEN), FILE_GS_TOKEN

# sheet details - spanish
SHEET = {'id': '1LW69o3iJeJZUGCrJ1HfX19gMZXQNR0jGNbvscB6zQQA',
         'name': 'content'}
topic = 'spanish'

# # sheet details - russian
# SHEET = {'id': '1GxmPiZsd0Z7n065ePXqhVbqsPlFC35KVBFi1VuiJ8f8',
#          'name': 'Russian2000'}
# topic = 'russian'

# # sheet details - french
# SHEET = {'id': '1aRSpyZKph2lu1ljfNAnIWci4raMwS4lPO-9DjAGx2HI',
#          'name': 'WordList'}
# topic = 'french'


def duplicates_join_drop(df, dup_col, join_col):
    tag_df = df.groupby(dup_col).agg(lambda r: ";".join(r[join_col]))
    df.loc[:, join_col] = tag_df.loc[df[dup_col], join_col].values
    df = df[df[dup_col].duplicated() == False]
    return df


def transfer_google():

    # get sheet content
    gs = Google(FILE_GS_CREDS, FILE_GS_TOKEN)
    df = gs.sheet_content(SHEET['id'], SHEET['name'], 4)
    print(df.head(10))

    # check
    assert len(df.index) > 0

    # add common key
    df.columns = ['question', 'answer', 'tag', 'alternatives']
    df['key'] = df.iloc[:, 0] + "|" + df.iloc[:, 1]
    df['tag'] = df['tag'].fillna('')
    df['alternatives'] = df['alternatives'].fillna('')
    df = duplicates_join_drop(df, 'key', 'tag')
    # df = df[df.key.duplicated() == False]
    df = df.reset_index()
    print(df.head(10))

    for r in range(df.shape[0]):
        print(r)
        row = df.iloc[r]
        print(row)
        # alts = row['alternatives'] is not None else ''
        item = Item(topic=topic,
                    index=row['index'],
                    question=row['question'],
                    answer=row['answer'],
                    key=row['key'],
                    tags=row['tag'], 
                    alts=row['alternatives'])
        print(item.question)
        item.save()


def test_duplicates_join_drop():
    df_in = pd.DataFrame({
        "key": ['a', 'a', 'b'],
        "tag": ["0", "2", "3"]
        })
    df_out = pd.DataFrame({
        "key": ['a', 'b'],
        "tag": ["0;2", "3"]
        })
    assert duplicates_join_drop(df_in, 'key', 'tag').reset_index(drop=True).equals(df_out)


# test_duplicates_join_drop()
