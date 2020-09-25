import sys
import pandas as pd
from utils import *


def get_issues_insights(oauth_token, repo_name):
    print('Getting issues insights')
    g = Github(oauth_token)
    repo = g.get_repo(repo_name)
    issues = repo.get_issues(state='all')
    #print(type(issues))
    data = []
    for issue in issues:
        issue_url = issue.url
        issue_created = issue.created_at
        issue_closed = issue.closed_at
        data.append([issue_url, issue_created, issue_closed])
        comments = issue.get_comments()
        for comment in comments:
            #print(comment.created_at)
            data.append([issue.url, comment.created_at, ])

    df = pd.DataFrame(data, columns=['issue', 'created_at', 'closed_at'])

    print(df)
    df.to_csv('../output/issues.csv', index=False)

if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_oauth_token = sys.argv[1]
        print('I need a repo to get insights from, and you didn\'t pass any')
        get_all_repos(my_oauth_token, '')

    elif len(sys.argv) == 3:
        my_oauth_token = sys.argv[1]
        my_repo = sys.argv[2]
        if get_all_repos(my_oauth_token, my_repo):
            df = get_issues_insights(my_oauth_token, my_repo)
            #history_clones('../output/issues.csv', df)
