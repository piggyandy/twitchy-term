#!/usr/bin/env python3

import curses
import json
import locale
import urllib.request, urllib.parse, urllib.error
import argparse
import os

import livestreamer

from .featured import FeaturedScreen
from .games import GamesScreen
from .streams import StreamsScreen
from .search import SearchScreen

from .util import SCREEN_CODE, QUALITY, DESCRIPTION, EPILOG

class TwitchyTerm(object):
    """
    Twitchy-Term class this class manages 
    all the screens
    """

    def __init__(self,args):

        self.idx = 0
        self.items_on_page = 0
        self.help = ""
        self.args = args

    def run(self):
        locale.setlocale(locale.LC_ALL, '')
        self.code = locale.getpreferredencoding()

        self.code = "utf-8"

        self.curses_main()

    def curses_main(self):
        self.screen = curses.initscr()
        curses.start_color()
        curses.noecho()
        self.screen.keypad(1)

        # check the screen size
        (h, w) = self.screen.getmaxyx()

        #initialize display
        curses.curs_set(0)
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(2, curses.COLOR_WHITE, -1)
        curses.init_pair(3, curses.COLOR_CYAN, -1)
        curses.init_pair(4, curses.COLOR_MAGENTA, -1)
        curses.init_pair(5, curses.COLOR_BLUE, -1)
        curses.init_pair(6, curses.COLOR_RED, -1)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_MAGENTA)

        # height of main_win is h-1 instead of h-2
        self.main_win = curses.newwin(h-1, w, 1, 0)
        self.main_win.keypad(1)
        self.main_win.bkgd(' ', curses.color_pair(3))
        self.top_bar = curses.newwin(1, w, 0, 0)
        self.top_bar.bkgd(' ', curses.color_pair(1))
        self.help_bar = curses.newwin(1, w, h-1, 0)
        self.help_bar.bkgd(' ', curses.color_pair(1))

        # init the screens
        self.featured_screen = FeaturedScreen(self)
        self.games_screen = GamesScreen(self)
        self.streams_screen = StreamsScreen(self)
        self.search_screen = SearchScreen(self)

        # start with featured screen
        self.featured_screen.get_feed()
        screen_code = self.featured_screen.loop()
        self.current = self.featured_screen

        while True:

            if screen_code == SCREEN_CODE['featured']:

                self.featured_screen.get_feed()

                self.featured_screen.args = self.current.args
                self.current = self.featured_screen
                self.current.resize_screen()
                screen_code = self.current.loop()

            elif screen_code == SCREEN_CODE['games']:

                self.games_screen.get_feed()

                self.games_screen.args = self.current.args
                self.current = self.games_screen
                self.current.resize_screen()
                screen_code = self.current.loop()

            elif screen_code == SCREEN_CODE['streams']:

                game_name = self.games_screen.game_name
                self.streams_screen.get_feed(game_name)

                self.streams_screen.args = self.current.args
                self.current = self.streams_screen
                self.current.resize_screen()
                screen_code = self.current.loop()

            elif screen_code == SCREEN_CODE['search']:

                query = self.search_screen.prompt_search()
                if query: 
                    self.search_screen.get_feed(query)
                    self.search_screen.args = self.current.args
                    self.current = self.search_screen

                self.current.resize_screen()
                screen_code = self.current.loop()

            elif screen_code == SCREEN_CODE['exit']:

                break
        
        curses.endwin()

def main():
    """
    Main function. This is where the program starts
    """

    # parse args
    parser = argparse.ArgumentParser(
        prog='twitchy-term', description=DESCRIPTION,
        epilog=EPILOG, formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('-q', '--quality', help='quality of VLC stream',
                        choices=QUALITY, default='best')

    args = parser.parse_args()

    # initialize
    tt = TwitchyTerm(args)
    tt.run()

if __name__ == "__main__":
    """
    https://gehrcke.de/2014/02/distributing-a-python-command-line-application/

    Following similar file structure to this tutorial. The only difference is 
    not using an extra python file for setup.py's entry point and just use __main__.py.
    """
    main()