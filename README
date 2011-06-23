First:
	You will need python version 3. If you don't already have it, download the
	latest version from python.org. You can check which version of python you
	have by typing `python -V`.
	
	All wrapper code is licensed to Skyler Leonard, under the terms of the GNU
	General Public License, either version 3 of the License, or
	(at your option) any later version. See the file COPYING for more
	information.
	
Installing:
	This package contains three python documents; wrap.py, instaopts.py and
	commands.py. To install the wrapper, copy all three to your server
	directory (the same as minecraft_server.jar). Now, instead of running
	minecraft_server.jar like you would normally, run `python3 wrap.py`.
	
Running:
	wrap.py take a few optional arguments:
	
	-h | --help
		Show usage information.
	
	-u | --unmute-keepup-warnings
		By default the wrapper will not print lines similar to
		"[WARNING] Can't keep up! Did the system time change, or is the server
			overloaded?".
		This option turns that feature off.
	
	-v | --verbose
		This option does nothing.
	
	-d | --dont-remove-ops
		By default the wrapper will delete all server operators, as found in
		ops.txt, letting itself handle who can use which commands. This
		option turns that feature off.
	
	-s | --server-dir server-dir
		Specify an alternative directory to find minecraft_server.jar in; by
		default use the current directory.
	
	-e | --server-options server-options
		Specify different options for the server options; by default use the
		options recommended on the website: "-Xmx1024M -Xms1024M"
	
	-i | --dir dir
		Specify a different directory to use for the wrapper option files, by
		default use 'wrap'.


The Wrapper:
	The wrapper adds many functions to minecraft:
	
		/item
			The /item command is similar to the built in /give command,
			however it is syntactically different, and allows for item black
			or white listing. The syntax is:
				/item (id or name) quantity [usernames]
			Item names can be found in the generated file 'items.txt'.
			[usernames] is optional, and defaults to the issuer of the
			command. The item list is a generated file, 'itemlist.txt', and
			wether to treat it as a black vs white list is specified in
			'settings.txt'.
		
		/kit
			The /kit command is like a batch /item. Kits specified in the
			'kits.txt' file can be received by a user by typing:
				/kit kitname
			
		/day and /night
			Shorthand for the built in /time command, /day will make it day
			(time is 0) and /night will make it night (time is 14000)
			
		/motd
			Display the Message Of The Day to the user. If 'motd on' is
			specified in 'settings.txt', also send it every time a user
			logs in.
			
		Money (/pay, /freemoney, /stats, /userstats)
			Each user can get a certain amount of money when they initially
			login. This amount is set in 'settings.txt'. The money unit e.g.
			'euros' is also set there. Users may give money to other users
			with the command /pay; syntax:
				/pay receiver amount
			Users can see their current money with the command /stats. One can
			see another's money with the command /userstats; syntax:
				/userstats username
			The command /freemoney will give money to the user who issues it;
			syntax:
				/freemoney amount
			
		/reboot
			Remotely reboot the server. This is the only command that does not
			check if a user has permissions to execute, because it uses a
			password, specified in 'settings.txt'. Syntax:
				/reboot password
			
			
Files:
	Included files:
		commands.py: A module that contains the code for executing commands.
		
		COPYING(.txt): The Gnu General Public License.
		
		instaopts.py: A module for easy command line options.
		
		README(.txt): This document.
		
		wrap.py: The main wrapper script.
	
	Generated files:
		itemlist.txt: The list of items to be white/black listed.
		
		items.txt: Item names.
		
		kits.txt: List of kits available to users.
		
		money.dat: A python pickled file containing money data.
		
		motd.txt: The Message Of The Day.
		
		settings.txt: Main configuration file.
		
		user.txt: File specifying which users can use which commands.