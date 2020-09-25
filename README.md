# insights_trough_api

The goal is to keep a history of github insights to be able to further manipulate the data provided.

There's an action ready, and it needs you to set up two secrets to access the repo you're interested to watch:

OAUTH: a personal token with read privileges
REPO: The full name of the repo you want insights from (:owner/:repo)

You should get a daily update of clones and views stats, and a weekly update of issues. The rationale is that
clones and views are queried since 15 days ago, so we need to keep rolling to be up to date.
On the other hand, issues are queried for all of them, so no need to keep up with dates.

