#!/usr/bin/env python
# encoding: utf-8
"""
    instaops.py
    Copyright (C) 2011  Skyler Leonard

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import sys, os
import getopt, string

def clone_dict(the_dict):
	"""Clone a dictionary, because nobody likes the copy module."""
	new = {}
	for key in the_dict:
		new[key] = the_dict[key]
	return new


class UsageError(Exception):
	"""Basic Exception for Usage Errors"""
	def __init__(self, msg):
		self.msg = msg

class Instaopts(object):
	"""Super easy option parsing, based on getopt. Just pass a dictionary of default values to __init__ and then check(sys.argv)
	
	fancy_help_message - use ansi escape seq to pretty up the help message. Default True.
	default_handling - handle errors the default way, which will interupt your program. If false, simply return None if there was an error.
	
	depends: getopt, string
	
	>>> options = {"verbose": False, "output": "file.out", "input": None}
	>>> opts = Instaopts(options)
	>>> opts.check(["script.py", "-v", "-o", "otherfile.out"]) == ({"verbose": True, "output": "otherfile.out", "input": None}, [])
	True
	>>> opts.check(["script.py", "-i", "somefile.in", "argfile.txt"]) == ({"verbose": False, "output": "file.out", "input": "somefile.in"}, ["argfile.txt"])
	True
	"""
	def __init__(self, options, fancy_help_message = True, default_handling = True):
		options.update({"help": False})
		self.default_handling = default_handling
		self.options = options
		self.__checkoptions()
		self.shorts = self.__makeshort()
		
		self.bools = []
		self.values = []
		for longe in self.options:
			if self.options[longe] in (True, False):
				self.bools.append(longe)
			else:
				self.values.append(longe)
				
		self.__fancy = {"normal": "\x1b[0m"*fancy_help_message, "underline": "\x1b[4m"*fancy_help_message}
		self.help_message = self.__make_help_message()
		
	def __checkoptions(self):
		"""Make sure all options are strings and not empty."""
		for opt in self.options:
			if not isinstance(opt, str) and opt:
				raise ValueError("Invalid Option: %s" % repr({opt: self.options[opt]}))
				
	def __makeshort(self):
		"""Make short options out of long ones"""
		shorts = {}
		for name in self.options:
			yes = False
			for let in name:
				if let in shorts:
					continue
				else:
					shorts[let] = name
					yes = True
					break
			if not yes:
				for let in string.ascii_letters:
					if let in shorts:
						continue
					else:
						shorts[let] = name
						yes = True
			if not yes:
				raise ValueError("Too many options!")
		return shorts
		
	def __getshort(self, longopt):
		"""get the short of specified long option"""
		for short in self.shorts:
			if self.shorts[short] == longopt:
				return short
		return None
	
	def __condensed(self):
		"""Make condensed short options; i.e. in the form "hvo:" """
		cond = ""
		for longe in self.bools:
			cond += self.__getshort(longe)
		for longe in self.values:
			cond += self.__getshort(longe) + ":"
		return cond
		
	def __list_opts(self):
		"""Make options into list for getopt"""
		liste = []
		for longe in self.bools:
			liste.append(longe)
		for longe in self.values:
			liste.append(longe + "=")
		return liste
		
	def __make_help_message(self):
		"""Create a help message"""
		msg = self.__fancy["normal"] + "\nUsage:"
		for boo in self.bools:
			msg += " [ -%s | --%s ]" % (self.__getshort(boo), boo)
		for value in self.values:
			msg += " [ -%s | --%s %s ]" % (self.__getshort(value), value, self.__fancy["underline"] + value + self.__fancy["normal"])
		return msg
	
	def check(self, argv, start = 1):
		"""Check args and return a new dict"""
		cond = self.__condensed()
		list_opts = self.__list_opts()
		options = self.options.copy()
		try:
			try:
				opts, args = getopt.getopt(argv[start:], cond, list_opts)
			except getopt.error as msg:
				raise UsageError(msg)
			
			for option, value in opts:
				if option[:2] == "--":
					# long option
					opt = option[2:]
				elif option[:1] == "-":
					# short option
					opt = self.shorts[option[1:]]
				
				if opt in self.bools:
					value = not self.options[opt]
				
				options[opt] = value
			
			if options["help"]:
				raise UsageError(self.help_message)
			
		except UsageError as err:
			if self.default_handling:
				print(sys.argv[0].split("/")[-1] + ":" + str(err.msg), file=sys.stderr)
				print("\t for help use --help", file=sys.stderr)
				sys.exit(2)
			else:
				return None
		
		del options["help"]
		
		return options, args

if __name__ == '__main__':
	import doctest
	doctest.testmod()
	
	