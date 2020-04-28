#!/usr/bin/env python3

# Note: run instructions
# python3 manage.py shell
# import [filename]

import os
import pandas as pd

from quizit.models import Response

# sheet details - spanish
base_path = '../data/'
print(os.listdir(base_path))
load_path = os.path.join(base_path, 'responses.xlsx')

def main():

    # get content
    resp_df = pd.read_excel(load_path)
    print(resp_df.head())

    # add common key
    for r in range(resp_df.shape[0]):
        print(r)
        row = resp_df.iloc[r]
        response = Response(topic=row['topic'],
                            correct=row['correct'],
                            key=row['key'],
                            ts=row['ts'],
                            user=row['user'])
        response.save()

# if __name__ == '__main__':
#     main()

main()