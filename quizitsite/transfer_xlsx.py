#!/usr/bin/env python3

# Note: run instructions
# python3 manage.py shell
# import [filename]

import os
import pandas as pd

from quizit.models import Item


def transfer_xlsx():
    
    # sheet details - spanish
    base_path = '../data/'
    try:
        print(os.listdir(base_path))
    except: 
        base_path = '/home/bitnami/apps/django/django_projects/QuizIt/data'
    path = os.path.join(base_path, 'spanish.xlsx')
    topic = 'spanish'   

    # get content
    df = pd.read_excel(path)
    print(df.head())

    # add common key
    df = df.iloc[:, 0:4]
    df.columns = ['question', 'answer', 'tag', 'alternatives']
    df['key'] = df.iloc[:, 0] + "|" + df.iloc[:, 1]
    df = df[df.key.duplicated() == False]
    df = df.reset_index()
    print(df.head(10))

    for r in range(df.shape[0]):
        print(r)
        row = df.iloc[r]
        item = Item(topic=topic,
                    index=row['index'],
                    question=row['question'],
                    answer=row['answer'],
                    key=row['key'],
                    tags=row['tag'], 
                    alts=row['alternatives'])
        print(item.question)
        item.save()

# MA: main() disabled, need to call transfer_xlsx() to initiate transfer
