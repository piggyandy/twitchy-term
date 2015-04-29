#!/usr/bin/env python3

import curses
import json
import sys
import urllib.request, urllib.parse, urllib.error

from .util import SCREEN_CODE, NO_RESULTS
from .base import ScreenBase


class SearchScreen(ScreenBase):

	def __init__(self,screen):

		super(SearchScreen, self).__init__()
		self.help = "'f':featured 'g':games 'p':play stream " \
					"'s':search 'c':change quality 'q':quit"

		self.copy_members(screen)

	def loop(self):

		self.idx = 0
		self.update_screen()

		while True:

			event = self.main_win.getch()

			if event == ord("q"):
				return SCREEN_CODE['exit']
			elif event == curses.KEY_UP:
				if self.idx > 0: 
					self.idx -= 1
					self.update_screen()
				elif self.idx == 0 and self.start_idx > 0:
					self.start_idx -= 1
					self.update_screen()
			elif event == curses.KEY_DOWN:
				if self.idx < (self.items_on_page-1): 
					self.idx += 1
					self.update_screen()
				elif (self.idx == (self.items_on_page-1) and
						(self.start_idx + self.items_on_page) < len(self.items.get('streams'))):
					self.start_idx += 1
					self.update_screen()
			elif event == curses.KEY_RESIZE:
				self.resize_screen()
			elif event == ord("f"):
				return SCREEN_CODE['featured']
			elif event == ord("g"):
				return SCREEN_CODE['games']
			elif event == ord("p"):
				self.play_stream()
			elif event == ord("s"):
				return SCREEN_CODE['search']
			elif event == ord("c"):
				self.change_quality()

		curses.endwin()

	def update_screen(self):

		(h,w) = self.main_win.getmaxyx()

		items_per_page = h // 2
		# One less item if height's even number. 
		# This is to prevent the addstr error of writing to 
		# window's bottom right position.
		if h % 2 is 0: items_per_page -= 1
		
		self.items_on_page = min(items_per_page, len(self.items.get('streams')))

		# readjusting purposes when decreasing term size
		selected_idx = self.start_idx + self.idx
		if self.idx > (self.items_on_page - 1):
			if self.start_idx > 0:
				self.start_idx = selected_idx - self.items_on_page + 1
			self.idx = self.items_on_page - 1

		# main window
		self.main_win.erase()

		if len(self.items.get('streams')) is 0:
			self.main_win.addnstr(0, 0, NO_RESULTS, len(NO_RESULTS), curses.color_pair(6))
			self.main_win.addnstr(self.query, len(self.query), curses.color_pair(3) | curses.A_BOLD)
			self.main_win.addnstr(".", 1, curses.color_pair(6))
		else:
			y = 0; n = 0
			x = self.start_idx
			for item in self.items.get('streams')[x:(x+self.items_on_page)]:	
				status = item.get('channel',{}).get('status')
				viewers = str(item.get('viewers'))
				game_name = item.get('game')
				display_name = item.get('channel',{}).get('display_name')

				
				if n == self.idx: 
					item1 = "%s" % (status)
					item2 = "%s playing %s with %s viewers" % (display_name, game_name, viewers)

					item1 = item1.ljust(w,' ')
					item2 = item2.ljust(w,' ')

					self.main_win.addstr(y, 0, item1, curses.color_pair(7))
					self.main_win.addstr(y + 1,0, item2, curses.color_pair(7))
				else:
					status = self.encode(status)
					display_name = self.encode(display_name)
					game_name = self.encode(game_name)

					self.main_win.addstr(y, 0, status,curses.color_pair(4) | curses.A_BOLD)
					self.main_win.addnstr(y + 1, 0, display_name, len(display_name), curses.color_pair(5))
					text = " playing "
					self.main_win.addnstr(text, len(text), curses.color_pair(2))
					self.main_win.addnstr(game_name, len(game_name), curses.color_pair(5))
					text = " with "
					self.main_win.addnstr(text, len(text), curses.color_pair(2))
					self.main_win.addnstr(viewers, len(viewers), curses.color_pair(5))
					text = " viewers"
					self.main_win.addnstr(text, len(text), curses.color_pair(2))


				y += 2
				n += 1

		self.main_win.refresh()

		# top bar
		self.top_bar.erase()
		self.top_bar.addstr(0, 0, "Search: %s" % self.query)
		self.top_bar.refresh()

		# help bar
		self.help_bar.erase()
		self.help_bar.addstr(0, 0, self.help[:(w-1)])
		self.help_bar.refresh()

	def get_feed(self,query):
		# replace space with +
		self.query = query
		query = query.replace(" ", "+")	
		url = "https://api.twitch.tv/kraken/search/streams?q=%s&limit=100" % (str(query))
		urllib.parse.quote(url)		

		response = urllib.request.urlopen(url)
		content = response.read().decode(self.code)
		self.items = json.loads(content)

	def get_stream_url(self):
		return self.items.get('streams')[self.idx].get('channel',{}).get('url')

	def prompt_search(self):
		(h, w) = self.screen.getmaxyx()

		self.help_bar.erase()
		self.help_bar.addstr(0, 0, 'search: ')
		self.help_bar.refresh()

		prompt_len = len('search: ')
		input_bar = curses.newwin(1, w-prompt_len, h-1, prompt_len)
		input_bar.bkgd(' ', curses.color_pair(1))
		curses.curs_set(1)
		curses.echo()
		try:
			s = input_bar.getstr(0,0)
			s = s.decode(self.code)
		except KeyboardInterrupt:
			s = None
		curses.noecho()
		curses.curs_set(0)

		return s