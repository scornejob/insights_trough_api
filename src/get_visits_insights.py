import sys
import os

import pandas as pd
from utils import *



def get_visits_insights(oauth_token, repo_name):
    print('Getting views insights')
    g = Github(oauth_token)
    repo = g.get_repo(repo_name)
    visits_traffic = repo.get_views_traffic()
    print(visits_traffic)
    #clones = clones_traffic['clones']

    # gt_df = []
    # for entry in clones:
    #     line = [entry.timestamp, entry.uniques, entry.count]
    #     gt_df.append(line)
    # gt_df = pd.DataFrame(gt_df, columns=['timestamp', 'uniques', 'count'])
    # print('Here\'s what we\'ve got today:')
    # print(gt_df.to_string())
    # return gt_df


def history_clones(file, ht_df):
    """
    here we write a csv file and append the new df
    :param file:
    :param ht_df:
    :return:
    """
    if os.path.isfile(file):
        # if the file exists, we merge
        print(file + ' found, merging')
        df_file = pd.read_csv(file)

        ht_df['timestamp'] = pd.to_datetime(ht_df['timestamp']).dt.date

        df_file = pd.concat([df_file, ht_df])
        df_file['timestamp'] = df_file['timestamp'].astype(str)

        df_file.sort_values('timestamp', inplace=True)
        df_file.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)

        df_file.to_csv(file, index=False)

    else:
        # otherwise, just dump the df
        print('There is no file to merge, dumping df to ' + file)
        ht_df.to_csv(file, index=False)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_oauth_token = sys.argv[1]
        print('I need a repo to get insights from, and you didn\'t pass any')
        get_all_repos(my_oauth_token, '')

    elif len(sys.argv) == 3:
        my_oauth_token = sys.argv[1]
        my_repo = sys.argv[2]
        if get_all_repos(my_oauth_token, my_repo):
            df = get_visits_insights(my_oauth_token, my_repo)
            history_clones('../output/views.csv', df)
