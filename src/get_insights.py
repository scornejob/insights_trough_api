import sys
import datetime as dt
import pandas as pd

from github import Github

def get_traffic(repo):
    repo = g.get_repo(repo)
    clones_traffic = repo.get_clones_traffic()
    #print(clones_traffic)
    count = clones_traffic['count']
    uniques = clones_traffic['uniques']
    clones = clones_traffic['clones']
    print('count: ' + str(count))
    print('uniques: ' + str(uniques))
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

    print(df)

if __name__ == '__main__':

    my_oauth_token = sys.argv[1]
    if len(sys.argv) == 2:
        since = dt.datetime.now()
        to = since - dt.timedelta(days=7)

        since = since.date()
        to = to.date()
        print('Retrieving insights from ' + str(since) + ' to ' + str(to))

        g = Github(my_oauth_token)

        for repo in g.get_user().get_repos():
            print(repo.name)

        user = g.get_user()
        print('Running as ' + user.name + '(for auth issues, you should have access to the repo you\'re interested in)')
        repo = 'MinCiencia/Datos-COVID19'
        get_traffic(repo)


    else:
        print('Silly... how can I access the API if I don have an oauth token?')
