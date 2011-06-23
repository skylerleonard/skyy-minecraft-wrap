#!/usr/bin/env python
# encoding: utf-8
"""
    wrap.py
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

import sys, os, threading, shlex, queue, subprocess, re, time
import instaopts
from commands import Commands

DEBUG = False

required_files = {
"settings.txt": "# This is the settings file\n\nitemlist blacklist\t\t\t# To treat the itemlist as a blacklist or whitelist\n\n# Money settings\ndefaultmoney 20    \t\t\t# The default money to give users\nmoneyunit coins    \t\t\t# The unit of exchange, e.g. 'euros'\n\nmotd on\t\t\t\t\t\t# To send the Message of the Day to users on login\n\nglobalcommands pay stats\t# global commands anyone can use\n\nrebootpassword 1c7ax\t\tThe password to remote reboot the server",
"users.txt": "# This is the users file, add users in the format <username> <allowed commands> ...\n# e.g. to allow \"Player\" to use the command `/help`:\n\nPlayer help    # You should probably delete this line later.",
"itemlist.txt": "# Add listed block ids here, one per line.\n#To change this file to a blacklist or whitelist see settings.txt\n\n7\n46",
"kits.txt": "# Add kits here in the form:\n# <kitname> <itemid>:<quantity> ...\n# <quantity> is optional, and defaults to 1\n\n# For instance this kit would give one Stone Pickaxe, and 64 Cobblestone:\nstarter 274 4:64",
# sorry about this stupid line.
"items.txt": 'Stone 01\nGrass 02\nDirt 03\nCobblestone 04\nWoodenPlank 05\nSapling 06\nBedrock 07\nWater 08\nStationarywater 09\nLava 10\nStationarylava 11\nSand 12\nGravel 13\nGoldOre 14\nIronOre 15\nCoalOre 16\nWood 17\nLeaves 18\nSponge 19\nGlass 20\nLapisLazuliOre 21\nLapisLazuliBlock 22\nDispenser 23\nSandstone 24\nNoteBlock 25\nBed 26\nPoweredRail 27\nDetectorRail 28\nCobweb 30\nTallGrass 31\nDeadShrubs 32\nWool 35\nDandelion 37\nRose 38\nBrownMushroom 39\nRedMushroom 40\nGoldBlock 41\nIronBlock 42\nDoubleSlabs 43\nSlabs 44\nBrickBlock 45\nTNT 46\nBookshelf 47\nMossStone 48\nObsidian 49\nTorch 50\nFire 51\nMonsterSpawner 52\nWoodenStairs 53\nChest 54\nRedstoneWire 55\nDiamondOre 56\nDiamondBlock 57\nCraftingTable 58\nSeeds 59\nFarmland 60\nFurnace 61\nBurningFurnace 62\nSignPost 63\nWoodenDoor 64\nLadders 65\nRails 66\nCobblestoneStairs 67\nWallSign 68\nLever 69\nStonePressurePlate 70\nIronDoor 71\nWoodenPressurePlate 72\nRedstoneOre 73\nGlowingRedstoneOre 74\nRedstoneTorch("off"state) 75\nRedstoneTorch("on"state) 76\nStoneButton 77\nSnow 78\nIce 79\nSnowBlock 80\nCactus 81\nClayBlock 82\nSugarCane 83\nJukebox 84\nFence 85\nPumpkin 86\nNetherrack 87\nSoulSand 88\nGlowstoneBlock 89\nPortal 90\nJack-O-Lantern 91\nCakeBlock 92\nRedstoneRepeaterOff 93\nRedstoneRepeaterOn 94\nLockedChest 95\nTrapdoor 96\nIronShovel 256\nIronPickaxe 257\nIronAxe 258\nFlintandSteel 259\nApple 260\nBow 261\nArrow 262\nCoal 263\nDiamond 264\nIronIngot 265\nGoldIngot 266\nIronSword 267\nWoodenSword 268\nWoodenShovel 269\nWoodenPickaxe 270\nWoodenAxe 271\nStoneSword 272\nStoneShovel 273\nStonePickaxe 274\nStoneAxe 275\nDiamondSword 276\nDiamondShovel 277\nDiamondPickaxe 278\nDiamondAxe 279\nStick 280\nBowl 281\nMushroomSoup 282\nGoldSword 283\nGoldShovel 284\nGoldPickaxe 285\nGoldAxe 286\nString 287\nFeather 288\nGunpowder 289\nWoodenHoe 290\nStoneHoe 291\nIronHoe 292\nDiamondHoe 293\nGoldHoe 294\nSeeds 295\nWheat 296\nBread 297\nLeatherCap 298\nLeatherTunic 299\nLeatherPants 300\nLeatherBoots 301\nChainHelmet 302\nChainChestplate 303\nChainLeggings 304\nChainBoots 305\nIronHelmet 306\nIronChestplate 307\nIronLeggings 308\nIronBoots 309\nDiamondHelmet 310\nDiamondChestplate 311\nDiamondLeggings 312\nDiamondBoots 313\nGoldHelmet 314\nGoldChestplate 315\nGoldLeggings 316\nGoldBoots 317\nFlint 318\nRawPorkchop 319\nCookedPorkchop 320\nPaintings 321\nGoldenApple 322\nSign 323\nWoodendoor 324\nBucket 325\nWaterbucket 326\nLavabucket 327\nMinecart 328\nSaddle 329\nIrondoor 330\nRedstone 331\nSnowball 332\nBoat 333\nLeather 334\nMilk 335\nClayBrick 336\nClay 337\nSugarCane 338\nPaper 339\nBook 340\nSlimeball 341\nStorageMinecart 342\nPoweredMinecart 343\nEgg 344\nCompass 345\nFishingRod 346\nClock 347\nGlowstoneDust 348\nRawFish 349\nCookedFish 350\nDye 351\nBone 352\nSugar 353\nCake 354\nBed 355\nRedstoneRepeater 356\nCookie 357\nMap 358\nGoldMusicDisc 2256\nGreenMusicDisc 2257',
"motd.txt": "Hello, World!",
"money.dat": "",
}

class Mod(object):
	"""The mod class"""
	def __init__(self, options):
		self.options = options
		self.commands = Commands(options) # from the module
		
		self.patterns = {
		r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \[INFO\] (.+) (?:tried|issued server) command: (.+)': self.command,
		r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \[INFO\] (.+) \[/(?:[0-9]{1,3}\.?){4}:[0-9]+\] logged in with entity id [0-9]+ at \((?:[0-9]+\.[0-9]+(?:, )?){3}\)': self.commands.userjoin,
		}
		
	def command(self, arg):
		"""Execute a command"""
		#print(arg)
		user, command, args = arg[0], shlex.split(arg[1])[0], shlex.split(arg[1])[1:]
		try:
			return self.commands.commands[command](*args, user=user)
		except KeyError as error:
			return []


def consoleinput(options, stopped, que):
	"""main loop for reading console input"""
	stopped.clear()
	while True:
		text = input()
		if stopped.is_set():
			break
		que.put(text)

def intoserver(options, server, que):
	"""main loop for data going into the server"""
	while True:
		text = que.get().encode() + b"\n"
		if server.returncode is not None:
			break
		server.stdin.write(text)
		server.stdin.flush()

def outofserver(options, mod, server, que, boot):
	"""main loop for data comeing out of server"""
	while True:
		if server.returncode is not None:
			break
		try:
			line = server.stdout.readline().decode()
		
			if (not options["unmute-keepup-warnings"]) and re.findall(r'^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2} \[WARNING\] Can\'t keep up! Did the system time change, or is the server overloaded\?', line):
				continue
		
			print(line, end="")
			
			for pattern in mod.patterns:
				result = re.findall(pattern, line)
				if result:
					for sendline in mod.patterns[pattern](result[0]):
						if sendline.split()[0] in ("reboot", ):
							boot.set()
							sendline = "stop"
						que.put(sendline)
			
		
		except UnicodeDecodeError as e:
			print(e)
		
		except Exception:
			if DEBUG:
				raise
			else:
				continue

def main(argv):
	opts = instaopts.Instaopts(
	{
		"unmute-keepup-warnings": False,
		"verbose": True,
		"dir": "./wrap",
		"server-dir": "./",
		"server-options": "-Xmx1024M -Xms1024M",
		"dont-remove-ops": False,
	})
	options, args = opts.check(argv)

	if not os.path.exists(os.path.join(options["server-dir"], "minecraft_server.jar")):
		print("Could not find minecraft-server.jar, perhaps you have the wrong server-dir?")
		return 1
	
	if not os.path.exists(options["dir"]):
		print("Could not find mod dir. Creating.")
		os.mkdir(options["dir"])
		
	for filename in required_files:
		if not os.path.exists(os.path.join(options["dir"], filename)):
			print("File %s not found. Creating." % filename)
			with open(os.path.join(options["dir"], filename), "w") as fileopen:
				fileopen.write(required_files[filename])
	
	if not options["dont-remove-ops"]:
		with open(os.path.join(options["server-dir"], "ops.txt"), "w") as opsfile:
			opsfile.write("")	
			
	datainto = queue.Queue(-1)
	
	boot = threading.Event()
	boot.set()
	
	stopped = threading.Event()
	
	try:
		import __main__
		mod = __main__.Mod(options)
	except ImportError:
		mod = Mod(options)
		
	threads = {}
		
	threads["consoleinput"] = threading.Thread(target=consoleinput, args=(options, stopped, datainto))
	
	threads["consoleinput"].start()
	
	while boot.is_set():
		
		boot.clear()
		
		server = subprocess.Popen(["java"] + shlex.split(options["server-options"]) + ["-jar", os.path.join(options["server-dir"], "minecraft_server.jar"), "nogui"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		
		threads["intoserver"] = threading.Thread(target=intoserver, args=(options, server, datainto))
		
		threads["outofserver"] = threading.Thread(target=outofserver, args=(options, mod, server, datainto, boot))
		
		for name in ["intoserver", "outofserver"]:
			threads[name].start()
		
		try:
			server.wait()
		except KeyboardInterrupt:
			datainto.put("stop")
			server.wait()
		
		while threads["intoserver"].is_alive():
			datainto.put("")
			time.sleep(.1)
	
	stopped.set()
	print("Server stopped, press enter to exit.", end="")
	return 0

if __name__ == '__main__':
	sys.exit(main(sys.argv))