#!/usr/bin/env python3

import curses
import json
import sys
import urllib.request, urllib.parse, urllib.error

from .util import SCREEN_CODE
from .base import ScreenBase


class GamesScreen(ScreenBase):
	"""
	Game screen showing differnet game categoies
	"""

	def __init__(self,screen):

		super(GamesScreen, self).__init__()
		self.help = "'f':featured 'e':select game " \
					"'s':search 'q':quit"

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
						(self.start_idx + self.items_on_page) < len(self.items.get('top'))):
					self.start_idx += 1
					self.update_screen()
			elif event == ord("f"):
				return SCREEN_CODE['featured']
			elif event == ord("e"):
				self.game_name = self.items['top'][self.idx]['game']['name']
				return SCREEN_CODE['streams']
			elif event == ord("s"):
				return SCREEN_CODE['search']
			elif event == curses.KEY_RESIZE:
				self.resize_screen()

		curses.endwin()

	def update_screen(self):

		(h,w) = self.main_win.getmaxyx()

		items_per_page = h // 2
		# One less item if height's even number. 
		# This is to prevent the addstr error of writing to 
		# window's bottom right position.
		if h % 2 is 0: items_per_page -= 1
		
		self.items_on_page = min(items_per_page, len(self.items.get('top')))

		# readjusting purposes when decreasing term size
		selected_idx = self.start_idx + self.idx
		if self.idx > (self.items_on_page - 1):
			if self.start_idx > 0:
				self.start_idx = selected_idx - self.items_on_page + 1
			self.idx = self.items_on_page - 1

		# main window
		self.main_win.erase()

		y = 0; n = 0
		x = self.start_idx
		for item in self.items.get('top')[x:(x+self.items_on_page)]:
			game_name = item.get('game',{}).get('name')
			viewers = str(item.get('viewers'))
			channels = str(item.get('channels'))

			if n == self.idx: 
				item1 = "%s" % (game_name)
				item2 = "%s viewers | %s channels" % (viewers,channels)	

				item1 = item1.ljust(w,' ')
				item2 = item2.ljust(w,' ')

				self.main_win.addstr(y, 0, item1,curses.color_pair(7))
				self.main_win.addstr(y+1, 0, item2,curses.color_pair(7))
			else:
				game_name = self.encode(game_name)

				self.main_win.addstr(y , 0, game_name,curses.color_pair(4) | curses.A_BOLD)
				self.main_win.addnstr(y+1, 0, viewers,len(viewers), curses.color_pair(5))
				
				text = " viewers | "
				self.main_win.addnstr(text, len(text), curses.color_pair(2))
				self.main_win.addnstr(channels, len(channels), curses.color_pair(5))
				text = " channels"
				self.main_win.addnstr(text, len(text), curses.color_pair(2))

			y += 2
			n += 1

		self.main_win.refresh()

		# top bar
		self.top_bar.erase()
		self.top_bar.addstr(0, 0, "Top Games")
		self.top_bar.refresh()

		# help bar
		self.help_bar.erase()
		self.help_bar.addstr(0, 0, self.help[:(w-1)])
		self.help_bar.refresh()

	def get_feed(self):
		url = "https://api.twitch.tv/kraken/games/top"

		response = urllib.request.urlopen(url)
		content = response.read().decode(self.code)
		self.items = json.loads(content)