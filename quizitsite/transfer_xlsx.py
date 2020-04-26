#!/usr/bin/env python3

# Note: run instructions
# python3 manage.py shell
# import [filename]

import os
import pandas as pd

from quizit.models import Item

# sheet details - spanish
base_path = '../data/'
print(os.listdir(base_path))
path = os.path.join(base_path, 'spanish.xlsx')
topic = 'spanish'

def main():

    # get content
    df = pd.read_excel(path)
    print(df.head())

    # add common key
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


# if __name__ == '__main__':
#     main()

main()