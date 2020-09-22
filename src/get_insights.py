import requests
import datetime as dt
import time


if __name__ == '__main__':
    since = dt.datetime.now()
    to = since - dt.timedelta(days=7)

    since = since.date()
    to = to.date()
    print('Retrieving insights from ' + str(since) + ' to ' + str(to))
