import requests

__plugin_author__ = "FirstName LastName"
__plugin_name__ = "test"
__plugin_version__ = 1
__plugin_welcome__ = "Sample plugin results"
__plugin_description__ = """
test feed
"""

__plugin_keywords__ = {"test", "france"}
__plugin_sources__ = {"example.com", }


def prepare():
    pass

def fetchNewEntries(last_fetch_date):
    return [{
            "url" : "http://example.com",
            "description": "Sample entry",
            "date" : last_fetch_date
        }]



