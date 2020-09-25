import sys
import pandas as pd
from utils import *


def get_visits_insights(oauth_token, repo_name):
    print('Getting views insights')
    g = Github(oauth_token)
    repo = g.get_repo(repo_name)
    visits_traffic = repo.get_views_traffic()
    views = visits_traffic['views']

    gt_df = []
    for entry in views:
        line = [entry.timestamp, entry.uniques, entry.count]
        gt_df.append(line)
    gt_df = pd.DataFrame(gt_df, columns=['timestamp', 'uniques', 'count'])
    print('Here\'s what we\'ve got today:')
    print(gt_df.to_string())
    return gt_df

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
