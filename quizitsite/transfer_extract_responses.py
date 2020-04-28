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
save_path = os.path.join(base_path, 'responses.xlsx')

def main():

    # extract response and convert to df
    responses = Response.objects.filter()
    resp_list = [r.to_dict() for r in responses]
    resp_df = pd.DataFrame(resp_list)

    # remove timezone from timestamp (which Excel doesn't like)
    resp_df['ts'] = resp_df['ts'].dt.tz_convert(None)

    # save to file
    resp_df.to_excel(save_path, index=False)


# if __name__ == '__main__':
#     main()

main()