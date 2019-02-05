import requests
from datetime import datetime

__plugin_author__ = "Olivier D"
__plugin_name__ = "HackerNews Jobs"
__plugin_version__ = 1
__plugin_welcome__ = "Latest jobs from HackerNews !"
__plugin_description__ = """
Prints the latest job offers from HackerNew API
"""
__plugin_dependencies__ = {}
__plugin_keywords__ = {"hn", "hacker", "news", "job", "jobs"}
__plugin_sources__ = {"hacker-news.firebaseio.com", }


def subscribed(data):
    print("Thank you for subscribing to " + __plugin_name__)

def fetchNewEntries(data, custom_deps, last_fetch_date):

    last_fetch_date = datetime.fromisoformat(last_fetch_date)

    jobids = requests.get("https://hacker-news.firebaseio.com/v0/jobstories.json").json()

    results = []

    for jobid in jobids:
        desc = requests.get("https://hacker-news.firebaseio.com/v0/item/%d.json" % jobid).json()
        date = datetime.utcfromtimestamp(desc["time"])

        if date > last_fetch_date:
            results.append({"url" : desc["url"],
                            "description" : desc["title"],
                            "date": date.isoformat()
                        })
    return results



