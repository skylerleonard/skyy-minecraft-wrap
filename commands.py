#!/usr/bin/env python
# encoding: utf-8
"""
    commands.py
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

import shlex, os, pickle

op_commands = ["?", "help", "kick", "ban", "pardon", "ban-ip", "pardon-ip", "op", "deop", "tp", "give", "stop", "save-all", "save-off", "save-on", "list", "say", "time", "whitelist"]

def loadfile(filename):
	"""Load a file"""
	data = {}
	with open(filename) as openfile:
		for line in openfile:
			line = line.split('#')[0]
			sp = shlex.split(line)
			if sp:
				data[sp[0]] = {el.split(":")[0]:(el.split(":")[1:] or [True, ])[0] for el in sp[1:]}
	return data

def quickread(filename):
	"""read text from a file"""
	with open(filename) as openfile:
		return openfile.read()

class Commands(object):
	"""Commands"""
	def __init__(self, options):
		self.options = options
		
		self.reload()
		
		self.money = Money(os.path.join(self.options["dir"], "money.dat"))
		
		self.commands = {
		"kit": self.kit,
		"item": self.item,
		"day": self.day,
		"night": self.night,
		"motd": self.motd,
		"pay": self.pay,
		"freemoney": self.freemoney,
		"stats": self.stats,
		"userstats": self.userstats,
		"reboot": self.reboot,
		}
		self.commands.update({ cmd:self.op_command for cmd in op_commands })
		
	def userjoin(self, user):
		"""What to do when a user joins the server"""
		if user not in self.users:
			self.users[user] = []
			with open(os.path.join(self.options["dir"], "users.txt"), "a") as userstxt:
				userstxt.write("\n" + user)
		
		with self.money:
			if user not in self.money.money:
				self.money.money[user] = int(list(self.settings["defaultmoney"])[0])
				
		if list(self.settings["motd"])[0] == "on":
			return self.motd(user=user)
		return []
		
	def __checkuser(self, command, user="Player"):
		"""Check if user is allowed to execute command"""
		try:
			if command in self.settings["globalcommands"] or command in self.users[user]:
				return True
			return False
		except KeyError:
			return False
			
	def op_command(self, *args, user="Player", command=""):
		"""function for not modded commands"""
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]
			
		return [command] + list(args)
		
	def reload(self, *args, user="Player"):
		"""Reload conf"""
		self.settings = loadfile(os.path.join(self.options["dir"], "settings.txt"))
		self.items = loadfile(os.path.join(self.options["dir"], "items.txt"))
		self.kits = loadfile(os.path.join(self.options["dir"], "kits.txt"))
		self.itemlist = loadfile(os.path.join(self.options["dir"], "itemlist.txt"))
		self.users = loadfile(os.path.join(self.options["dir"], "users.txt"))
		self.motd_text = quickread(os.path.join(self.options["dir"], "motd.txt")).split("\n")
		
	def kit(self, *kitnames, user="Player", command="kit"):
		"""docstring for kit"""
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]
			
		final = []
		for kitname in kitnames:
			try:
				for item in self.kits[kitname]:
					final.append("give {user} {item} {quant}".format(user=user, item=item, quant=int(self.kits[kitname][item])))
			except KeyError:
				final.append("tell {user} MSG: There's no kit with name {kitname}".format(user=user, kitname=kitname))
		return final
		
	def item(self, itemid, quantity, *sendusers, user="Player", command="item"):
		"""Give sendusers quantity of itemid"""
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]
			
		if not sendusers:
			sendusers = [user]
			
		if not itemid.isdigit():
			try:
				print(itemid)
				itemid = list(self.items[itemid])[0]
			except KeyError as error:
				print("KeyError:", error)
				return []
				
		if (list(self.settings["itemlist"])[0] == "whitelist") != (itemid in self.itemlist):
			return []
		return ["give {name} {itemid} {quantity}".format(name=name, itemid=itemid, quantity=quantity) for name in sendusers]
		
	def day(self, *args, user="Player", command="day"):
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]
		return ["time set 0"]
		
	def night(self, *args, user="Player", command="night"):
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]	
		return ["time set 14000"]
		
	def motd(self, *args, user="Player", command="motd"):
		return ["tell {user} MSG: MOTD: {motd}".format(user=user, motd=text) for text in self.motd_text]
	
	def pay(self, payto, amount, user="Player", command="pay"):
		"""send money from one player to another"""
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]
			
		amount = abs(int(amount)) # don't give people negative money...
		
		with self.money:
			if self.money.money[user] < amount:
				return ["tell {user} MSG: You do not have enough money!".format(user=user)]
			
			if payto not in self.money.money:
				return ["tell {user} MSG: No player named {payto}.".format(user=user, payto=payto)]
			
			self.money.money[user] -= amount
			self.money.money[payto] += amount
			return [
			"tell {user} MSG: You paid {payto} {amount} {unit}".format(user=user, payto=payto, amount=amount, unit=list(self.settings["moneyunit"])[0]),
			"tell {payto} MSG: {user} paid you {amount} {unit}".format(user=user, payto=payto, amount=amount, unit=list(self.settings["moneyunit"])[0]),
			]
	def freemoney(self, amount, user="Player", command="freemoney"):
		"""Give free money to user"""
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]
		
		amount = int(amount)
		
		with self.money:
			self.money.money[user] += amount
			
		return ["tell {user} MSG: You found {amount} {unit} laying on the ground.".format(user=user, amount=amount, unit=list(self.settings["moneyunit"])[0])]

	def userstats(self, username, user="Player", command="userstats"):
		"""Display user statistics"""
		if not self.__checkuser(command, user):
			return ["tell {user} MSG: You may not use that command!".format(user=user)]
		
		with self.money:
			try:
				return ["tell {user} MSG: Money: {money} {moneyunit}".format(user=user, money=self.money.money[username], moneyunit=list(self.settings["moneyunit"])[0])]
			except KeyError as e:
				return ["tell {user} MSG: That user has no stats.".format(user=user)]
			
			
	def stats(self, *args, user="Player", command="stats"):
		return self.userstats(username=user, user=user, command="stats")
		
	def reboot(self, password, user="Player", command="reboot"):
		"""Reboot the server"""
		if password == list(self.settings["rebootpassword"])[0]:
			return ["reboot"]
		return ["tell {user} MSG: incorect password".format(user=user)]


class Money(object):
	"""basic Money object"""
	def __init__(self, filename):
		self.filename = filename
		self.money = None
	def __enter__(self):
		with open(self.filename, "rb") as moneyfile:
			try:
				self.money = pickle.load(moneyfile)
			except EOFError:
				self.money = {}
	def __exit__(self, exc_type, exc_value, traceback):
		with open(self.filename, "wb") as moneyfile:
			pickle.dump(self.money, moneyfile)











