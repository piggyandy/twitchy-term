#!/usr/bin/env python3

import time
import curses
import json
import urllib.request, urllib.parse, urllib.error

from .util import SCREEN_CODE, QUALITY
from .base import ScreenBase


class FeaturedScreen(ScreenBase):
	"""
	Featured screen. The front page of Twitch.tv
	"""

	def __init__(self,screen):

		super(FeaturedScreen, self).__init__()
		self.help = "'g':games 'p':play stream " \
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
						(self.start_idx + self.items_on_page) < len(self.items.get('featured'))):
					self.start_idx += 1
					self.update_screen()
			elif event == curses.KEY_RESIZE:
				self.resize_screen()
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

		self.items_on_page = min(items_per_page, len(self.items.get('featured')))

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
		for item in self.items.get('featured')[x:(x+self.items_on_page)]:
			title = item.get('title')
			display_name = item.get('stream',{}).get('channel',{}).get('display_name')
			game_name = item.get('stream',{}).get('game')

			if n == self.idx: 
				# make string of each item
				item1 = "%s" % (title)
				item2 = "%s playing %s" % (display_name, game_name)

				# item1 = self.encode(item1).ljust(w, ' ')
				# item2 = self.encode(item2).ljust(w, ' ')
				item1 = item1.ljust(w, ' ')
				item2 = item2.ljust(w, ' ')

				self.main_win.addstr(y, 0, item1,curses.color_pair(7) | curses.A_BOLD)
				self.main_win.addstr(y+1, 0, item2,curses.color_pair(7))
			else:
				title = self.encode(title)
				display_name = self.encode(display_name)
				game_name = self.encode(game_name)

				self.main_win.addstr(y, 0, title,curses.color_pair(4) | curses.A_BOLD)
				self.main_win.addnstr(y+1, 0, display_name, len(display_name), curses.color_pair(5))
				text = " playing "
				self.main_win.addnstr(text, len(text), curses.color_pair(2))
				self.main_win.addnstr(game_name, len(game_name), curses.color_pair(5))

			y += 2
			n += 1

		self.main_win.refresh()

		# top bar
		self.top_bar.erase()
		self.top_bar.addstr(0, 0, "Featured Games")
		self.top_bar.refresh()

		# help bar
		self.help_bar.erase()
		self.help_bar.addstr(0, 0, self.help[:(w-1)])
		self.help_bar.refresh()

	def get_feed(self):
		url = "https://api.twitch.tv/kraken/streams/featured"
		response = urllib.request.urlopen(url)
		content = response.read().decode(self.code)
		self.items = json.loads(content)

	def get_stream_url(self):
		return (self.items.get('featured')[self.idx]
			.get('stream',{}).get('channel',{}).get('url'))