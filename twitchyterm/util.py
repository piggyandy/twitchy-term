#!/usr/bin/env python3

import os

STREAM_ERR = b"The specified stream\(s\) \'\w*\' could not be found."

NO_RESULTS = "No results found for "

SCREEN_CODE = {
    "exit": -1,
    "featured": 0,
    "games": 1,
    "streams": 2,
    "search": 3
}

QUALITY = [
    "best",
    "high",
    "medium",
    "low",
    "worst"
]

DESCRIPTION = """
TwitchyTerm
======================================================
A simple command line interface for browsing Twitch.tv 
and watch streams on VLC Player using Livestreamer.
"""

# might add stuff later
EPILOG = ""

def log(output):
    """Used for debugging purposes"""

    f = open('log.txt','a')
    f.write(output) 
    f.close() 

def console(output):
    print("[twitchy-term] %s" % output)