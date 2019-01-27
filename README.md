# Yourfeeds

Yourfeeds (yrfd) allows you to pull new entries from feeds that you choose.

Feeds are programmatically defined in the branch yourfeeds-plugins of this repository.

The idea is that everybody can contribute to the plugin database if they respect certain conditions.

You can of course, have your own plugins and plugins repository

[![asciicast](https://asciinema.org/a/41bslOc4JFmamIytm3l19C3O7.svg)](https://asciinema.org/a/41bslOc4JFmamIytm3l19C3O7)

# Install

    $ git clone https://github.com/Ododo/yourfeeds.git --branch master --single-branch
    
    $ cd yourfeeds && sudo pip3 install -r requirements.txt && sudo python3 setup.py install
    
    $ yrfd -u
  
    
usage: yrfd [-h] [-s SEARCH] [-d] [-u] [-U]


optional arguments:

    -h, --help            show this help message and exit

    -s SEARCH, --search SEARCH
                          Search a feed in our database

    -d, --unsubscribe     Unsubscribe to a feed

    -u, --update-plugins  Search for new plugins(feeds) in remote repository
    
# Writing plugins

Plugins are stored in a [particular branch](https://github.com/Ododo/yourfeeds/tree/yourfeeds-plugins),
you can start with the [exemple plugin](https://github.com/Ododo/yourfeeds/blob/yourfeeds-plugins/test_plugin.py)

Plugins must define:

```python
__plugin_author__ = "FirstName LastName"
__plugin_name__ = "Name for your plugin"
__plugin_version__ = 1
__plugin_welcome__ = "Welcome message to be printed each time the user pulls data from it"
__plugin_description__ = "Plugin desc."
__plugin_dependencies__ = {"dep1", "dep2"} # Custom dependencies (from pip) that will be loaded only if the user has subscribed to your feed 
__plugin_keywords__ = {"keyword1", "keyword12"}
__plugin_sources__ = {"example.com", "youtube.com"} # Urls that will be requested by your plugin 


def subscribed(data):
    """
    Called when the user just subscribed to your feed
    data is a dict object that you can use to store plugin data.
    """
    pass

def fetchNewEntries(data, custom_deps, last_fetch_date):
    """
    Called each time the user wants to fetch new entries from your plugin.
    
    data is the same object that in subscribed function.
    
    custom_deps is a dict. in which is stored all your imported custom dependencies
    from __plugin_dependencies__.
    
    last_fetch_date is a string in isoformat (UTC), representing the last time
    the user has executed this function. see https://docs.python.org/3/library/datetime.html#datetime.date.fromisoformat
    You may want to select entries whose date is > last_fech_date.
    """
    return [{
            "url" : "http://example.com", #the url of the entry
            "description": "Sample entry",
            "date" : last_fetch_date #the date of the entry in isoformat UTC (same format as last_fetch_date)
        }]
```

# Contributing

For contributing to the plugin database simply make a pull request on the *yourstream-plugins* branch once
you have written your plugin under the *plugins* folder.

For contributing to the yrfd core code make a pull request on the *master* branch.


# Data

yrfd stores plugins, python virtualenv and a json database in the *~/.yourfeeds* folder

