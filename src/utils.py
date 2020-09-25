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