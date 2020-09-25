import sys
import os
import datetime as dt
import pandas as pd

from github import Github

def get_all_repos(oauth_token, repo_name):
    '''
    The repo given by the user should be in the list
    :param oauth_token:
    :return:
    '''
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

def get_traffic(oauth_token, repo_name):
    print('Getting traffic insights')
    g = Github(oauth_token)
    repo = g.get_repo(repo_name)
    clones_traffic = repo.get_clones_traffic()
    #print(clones_traffic)
    count = clones_traffic['count']
    uniques = clones_traffic['uniques']
    clones = clones_traffic['clones']
    #print('count: ' + str(count))
    #print('uniques: ' + str(uniques))
    #print(clones)
    #print(type(clones))
    df = []
    for entry in clones:
        line = []
        #print(entry)
        line.append(entry.timestamp)
        line.append(entry.uniques)
        line.append(entry.count)
        #print(line)
        df.append(line)
    df = pd.DataFrame(df, columns=['timestamp', 'uniques', 'count'])

    #print(df)
    return df

def history_traffic(file, df):
    '''
    here we write a csv file and append the new df
    :param file:
    :param df:
    :return:
    '''
    if os.path.isfile(file):
        # if the file exists, we merge
        print(file +' found, merging')
        df_file = pd.read_csv(file)
        #df_file['timestamp'] = pd.to_datetime(df_file['timestamp']).dt.date
        print(df_file.dtypes)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.date
        print(df.dtypes)
        df_file = pd.concat([df_file, df])
        df_file['timestamp'] = df_file['timestamp'].astype(str)
        print(df_file)
        df_file.sort_values('timestamp', inplace=True)
        df_file.drop_duplicates(subset=['timestamp'], keep='last', inplace=True)
        print(df_file)
        df_file.to_csv(file, index=False)

    else:
        # otherwise, just dump the df
        print('There is no file to merge, dumping df to ' + file)
        df.to_csv(file, index=False)


if __name__ == '__main__':

    if len(sys.argv) == 2:
        my_oauth_token = sys.argv[1]
        print('I need a repo to get insights from, and you didn\'t pass any')
        get_all_repos(my_oauth_token, '')

    elif len(sys.argv) == 3:
        my_oauth_token = sys.argv[1]
        my_repo = sys.argv[2]
        if get_all_repos(my_oauth_token, my_repo):
            df = get_traffic(my_oauth_token, my_repo)
            history_traffic('../output/traffic.csv', df)

