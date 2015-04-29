#!/usr/bin/env python3

import curses
import time
import re

from subprocess import Popen, PIPE
from .util import *

class ScreenBase(object):
	"""
	Base class for a screen
	"""

	def __init__(self):
		self.items_on_page = 0
		self.idx = 0
		self.start_idx = 0

	def copy_members(self,screen):
		self.screen = screen.screen
		self.main_win = screen.main_win
		self.top_bar = screen.top_bar
		self.help_bar = screen.help_bar
		self.code = screen.code
		self.args = screen.args

	def encode(self,item):
		if item is not None:
			item = item.encode(self.code, 'replace')
		else:
			item = "None"
		return item

	def play_stream(self):

		curses.endwin()
		
		url = self.get_stream_url()
		quality = self.args.quality
		
		process = Popen(['livestreamer', url, quality], stdout=PIPE)
		console("Opening stream %s in %s quality." % (url, quality))
		output = process.communicate()[0]

		#Popen(['livestreamer', url, quality]).wait()
		
		if re.search(STREAM_ERR, output):
			console("The specified quality stream could not be found. " \
				"Streaming the best quality instead.")
			process = Popen(['livestreamer', url, 'best'], stdout=PIPE).communicate()

		self.update_screen()

	def resize_screen(self):
		"""
		Resize curses screens by deleting all windows and re-creating
		all from scratch
		"""
		# http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python 
		(h, w) = os.popen('stty size', 'r').read().split()
		h = int(h)
		w = int(w)

		del self.main_win
		del self.top_bar
		del self.help_bar

		curses.endwin()

		self.main_win = curses.newwin(h-1, w, 1, 0)
		self.main_win.keypad(1)
		self.main_win.bkgd(' ', curses.color_pair(3))
		self.top_bar = curses.newwin(1, w, 0, 0)
		self.top_bar.bkgd(' ', curses.color_pair(1))
		self.help_bar = curses.newwin(1, w, h-1, 0)
		self.help_bar.bkgd(' ', curses.color_pair(1))
		
		self.update_screen()

	def change_quality(self):

		(h, w) = self.screen.getmaxyx()

		self.help_bar.erase()
		self.help_bar.addstr(0, 0, 'enter new stream quality: ')
		self.help_bar.refresh()

		prompt_len = len('enter new stream quality: ')
		input_bar = curses.newwin(1, w-prompt_len, h-1, prompt_len)
		input_bar.bkgd(' ', curses.color_pair(1))
		curses.curs_set(1)
		curses.echo()

		try:
			s = input_bar.getstr(0,0).decode(self.code)

			curses.noecho()
			curses.curs_set(0)

			if s:
				if s in QUALITY:
					self.args.quality = s
					self.help_bar.erase()
					self.help_bar.addstr(0, 0, 'Quality has been set to: %s' % s)
					self.help_bar.refresh()
					time.sleep(2)
				else:
					self.help_bar.erase()
					self.help_bar.addstr(0, 0, 'ERROR: quality does not exist.')
					self.help_bar.refresh()
					time.sleep(2)
		except KeyboardInterrupt:
			s = None

		self.update_screen()