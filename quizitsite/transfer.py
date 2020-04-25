#!/usr/bin/env python3

# Note: run instructions
# python3 manage.py shell
# import transfer



from quizit.models import Item
from google_helper import Google

# credentials
FILE_GS_CREDS = '../../../credentials/google_sheets_credentials.json'
FILE_GS_TOKEN = '../../../credentials/google_sheets_token.pickle'

# sheet details - spanish
SHEET = {'id': '1LW69o3iJeJZUGCrJ1HfX19gMZXQNR0jGNbvscB6zQQA',
         'name': 'WordList'}
topic = 'spanish'

# # sheet details - russian
# SHEET = {'id': '1GxmPiZsd0Z7n065ePXqhVbqsPlFC35KVBFi1VuiJ8f8',
#          'name': 'Russian2000'}
# topic = 'russian'

# # sheet details - french
# SHEET = {'id': '1aRSpyZKph2lu1ljfNAnIWci4raMwS4lPO-9DjAGx2HI',
#          'name': 'WordList'}
# topic = 'french'


def main():

    # get sheet content
    gs = Google(FILE_GS_CREDS, FILE_GS_TOKEN)
    df = gs.sheet_content(SHEET['id'], SHEET['name'], 3)
    print(df.head(10))

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