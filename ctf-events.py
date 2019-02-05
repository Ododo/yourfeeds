import requests
from datetime import datetime

__plugin_author__ = "Olivier D"
__plugin_name__ = "CTF Events"
__plugin_version__ = 1
__plugin_welcome__ = "Upcoming CTF events"
__plugin_description__ = """
Prints the upcoming capture-the-flag events using ctftime.org API
"""
__plugin_dependencies__ = {}
__plugin_keywords__ = {"hacker", "ctf", "capture", "the", "flag", "security", "hack"}
__plugin_sources__ = {"hacker-news.firebaseio.com", }


def subscribed(data):
    print("Thank you for subscribing to " + __plugin_name__)

def fetchNewEntries(data, custom_deps, last_fetch_date):

    last_fetch_date = datetime.fromisoformat(last_fetch_date)

    ts = int(last_fetch_date.timestamp())
    headers = {"User-Agent" : "YRFD"}

    r = requests.get("http://ctftime.org/api/v1/events/?limit=10&start=%d" % ts, 
                     headers=headers)
    events = r.json()

    results = []

    for e in events:
        date = datetime.fromisoformat(e["start"]).replace(tzinfo=None)

        if date > last_fetch_date:
            results.append({"url" : e["ctftime_url"],
                            "description" : e["title"] + "\n" + e["description"],
                            "date": date.isoformat(),
                            "exclude_next" : True
                        })
    return results



