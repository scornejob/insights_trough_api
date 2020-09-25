import os
import pandas as pd

from github import Github

def get_all_repos(oauth_token, repo_name):
    """
    The repo given by the user should be in the list
    :param repo_name:
    :param oauth_token:
    :return:
    """
    print('Checking if the user can access the repo...')
    g = Github(oauth_token)
    print('\tRunning as ' + g.get_user().name)
    all_repos = g.get_user().get_repos()
    all_repos_full_name = []
    for test in list(all_repos):
        all_repos_full_name.append(test.full_name)
    if repo_name in all_repos_full_name:
        return True
    else:
        print('Repo "' + repo_name + '" is not in the list')
        print('Here\'s a list of all repos I can see:')
        for each_repo in all_repos:
            print('\t' + each_repo.full_name)
        return False


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
        print(df_file.to_string())
        # we can't just drop the first instance: for the first day, we'll loose data.
        # so keep max value per date

        #df_file.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
        df_file = df_file.groupby('timestamp')[['uniques', 'count']].agg(['max']).reset_index()

        df_file.columns = df_file.columns.droplevel(level=1)
        #print(df_file.to_string())
        #print(df_file.columns)
        df_file.to_csv(file, index=False)

    else:
        # otherwise, just dump the df
        print('There is no file to merge, dumping df to ' + file)
        ht_df.to_csv(file, index=False)