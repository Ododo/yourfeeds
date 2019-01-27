#!/usr/bin/python3

import sys
import subprocess
import argparse
import traceback

from os import getenv, path
from os import name as osname
from datetime import datetime, timezone

import json

import requests 

import plugins


PLUGIN_ATTRS = ("__plugin_name__", "__plugin_author__", "__plugin_version__", 
                "__plugin_description__", "__plugin_sources__", "__plugin_keywords__", 
                "fetchNewEntries")

YRFD_PATH = path.join(getenv("HOME"), ".yourfeeds/")
HISTORY_PATH = path.join(YRFD_PATH, "yrfd.json")

feeds = {}


def get_date():
    return datetime.utcnow()

def make_json(o):
    if isinstance(o, datetime):
        return o.isoformat()
    return json.JSONEncoder.default(obj)

def register_plugin(module):
    assert(all(e in module.__dict__ for e in PLUGIN_ATTRS))
    assert(all(e.islower() for e in module.__plugin_keywords__))
    feeds[module.__plugin_name__] = module

def search_plugin(keywords):
    return [s for s in feeds.values() if s.__plugin_keywords__.intersection(keywords)]

def build_database():
    return [register_plugin(p) for p in plugins.get_plugins()]

def print_welcome(welcome):
    print(welcome)

def print_search_results(results):
    print("\033[4mHere is the the list of feeds that matches your query:\033[0m")
    for i,r in enumerate(results):
        print("\033[93m{}\033[0m.\033[1m{}\033[0m".format(i, r.__plugin_name__))
        print(r.__plugin_description__)
        print("----")

def print_feed_results(results, offset):
    for i, r in enumerate(results):
        print("\033[93m{}\033[0m.\033[1m{}\033[0m".format(i+offset, r["description"]))
        utc_date = datetime.fromisoformat(r["date"])
        local_date = utc_date.replace(tzinfo=timezone.utc).astimezone(tz=None)
        print(r["url"], "(\033[94m%s\033[0m)" % local_date.strftime("%m/%d/%y %I:%M %p"))
    print("----")

def load_hist():
    open(HISTORY_PATH, "a").close()
    with open(HISTORY_PATH, "r") as fp:
        try:
            return json.load(fp)
        except json.decoder.JSONDecodeError:
            hist = {"subscribed_feeds" : {}}
            return hist

def save_hist(hist):
    with open(HISTORY_PATH, "w") as fp:
        json.dump(hist, fp, default=make_json)

def open_url(url):
    if sys.platform.startswith('darwin'):
        subprocess.call(('open', url))
    elif osname == 'nt':
        from os import startfile
        startfile(url)
    elif osname == 'posix':
        subprocess.call(('xdg-open', url))

def banner():
    return """╦ ╦┌─┐┬ ┬┬─┐╔═╗┌─┐┌─┐┌┬┐┌─┐
╚╦╝│ ││ │├┬┘╠╣ ├┤ ├┤  ││└─┐
 ╩ └─┘└─┘┴└─╚  └─┘└─┘─┴┘└─┘"""

def main():
    print("\033[1m\033[36m%s\033[0m" % banner())
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", help="Search a feed in our database")
    parser.add_argument("-d", "--unsubscribe", action="store_true", help="Unsubscribe to a feed")
    parser.add_argument("-u", "--update-plugins", action="store_true", help="Search for new plugins(feeds) in remote repository")
    parser.add_argument("-U", "--update-all", action="store_true", help="Update both executable and plugins database from remote repository")

    args = parser.parse_args()

    build_database()

    hist = load_hist()

    if args.search:
        keywords = set(args.search.lower().split())
        results = search_plugin(keywords)
        if not results:
            print("No feed matches your query !")
            return
        print_search_results(results)
        choice = int(input("Enter feed number to subscribe: "))
        name = results[choice].__plugin_name__
        if name not in hist["subscribed_feeds"]:
            hist["subscribed_feeds"][name] = {"last_fetch" : get_date(), 
                                              "old_entries" : []}
        else:
            print("Already subscribed to that feed")

    elif args.unsubscribe:
        tmp = list(hist["subscribed_feeds"])
        for i, name in enumerate(tmp):
            print("\033[93m%s\033[0m." % i, name)
        if tmp:
            choice = int(input("Enter feed number to unsubscribe: "))
            del hist["subscribed_feeds"][tmp[choice]]
        else:
            print("No subscribed feed")

    elif args.update_plugins:
        print("\033[32m\033[1mFetching new plugins from remote repository...\033[0m")
        for cmd in [("git", "checkout", "yourfeeds-plugins"),
                    ("git", "pull", "origin", "yourfeeds-plugins"),
                    ("git", "checkout", "master")]:
            if subprocess.call(cmd, cwd=YRFD_PATH):
                break

    elif args.update_all:
        print("\033[32m\033[1mUpdating YourFeeds from remote repository...\033[0m")
        for cmd in [("git", "checkout", "master"),
                    ("git", "pull", "origin", "master")]:
            if subprocess.call(cmd, cwd=YRFD_PATH):
                break
    else:
        results = []
        for name in hist["subscribed_feeds"]:
            feed = feeds[name]
            last_fetch_date = hist["subscribed_feeds"][name]["last_fetch"]
            old_entries = hist["subscribed_feeds"][name]["old_entries"]
            try:
                print_welcome("\033[4m" + feed.welcomeMessage() + "\033[0m")
                ret = feed.fetchNewEntries(last_fetch_date)
                for entry in ret: entry["origin"] = name
                ret.extend(old_entries)
                ret.sort(key = lambda x:datetime.fromisoformat(x["date"]), reverse=True)
                print_feed_results(ret, len(results))
                results.extend(ret)
                hist["subscribed_feeds"][name]["last_fetch"] = get_date()
                hist["subscribed_feeds"][name]["old_entries"] = ret
            except Exception as err:
                print("Feed \033[1m%s\033[0m failed to retreive new items, reason is :" % name)
                traceback.print_tb(err.__traceback__)
                continue

        if results:
            choice = int(input("Enter item number to open: "))
            entry = results[choice]
            open_url(results[choice]["url"])
            hist["subscribed_feeds"][entry["origin"]]["old_entries"].remove(entry)
        else:
            print("No subscribed feed, start by searching in the plugin database with 'yrfd -s string'")
    save_hist(hist)

if __name__ == "__main__":
    main()
