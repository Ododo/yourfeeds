import requests
import json
from datetime import datetime

__plugin_author__ = "Olivier D."
__plugin_name__ = "Guillaume Meurice sur France Inter"
__plugin_version__ = 1
__plugin_welcome__ = "Les dernières chroniques de Guillaume Meurice !"
__plugin_description__ = """
Récupère les derniers Meurice sur la chaine youtube de france inter
"""

__plugin_dependencies__ = {}
__plugin_keywords__ = {"guillaume", "meurice", "france", "inter"}
__plugin_sources__ = {"youtube.com", }

API_KEY=None


def subscribed(data):
    if not "API_KEY" in data:
        data["API_KEY"] = input("Please specify Youtube API_KEY to use plugin: ")
    API_KEY = data["API_KEY"]

def fetchNewEntries(last_fetch_date):
    last_fetch_date = datetime.fromisoformat(last_fetch_date) #utc
    r = requests.get("https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=25&q=le moment meurice&key=%s" % API_KEY)
    data = r.json()["items"]
    entries = []

    for e in data:
        if e["id"]["kind"] != "youtube#video":
            continue
        channelId = e["snippet"]["channelId"]
        publishedAt = e["snippet"]["publishedAt"][:-1] #remove Z (utc date)
        vid = e["id"]["videoId"]
        desc = e["snippet"]["description"]

        if channelId == "UCJldRgT_D7Am-ErRHQZ90uw" and datetime.fromisoformat(publishedAt) > last_fetch_date:
            entries.append({"url": "https://www.youtube.com/watch?v=%s" % vid,
                            "description" : desc,
                            "date" : publishedAt
                            })
    return entries

