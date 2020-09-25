import sys
import pandas as pd

from utils import *


def get_clones_insights(oauth_token, repo_name):
    print('Getting clones insights')
    g = Github(oauth_token)
    repo = g.get_repo(repo_name)
    clones_traffic = repo.get_clones_traffic()
    clones = clones_traffic['clones']

    gt_df = []
    for entry in clones:
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
            df = get_clones_insights(my_oauth_token, my_repo)
            history_clones('../output/clones.csv', df)
