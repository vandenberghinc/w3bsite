#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# classes imports.
from classes.config import *
from classes import utils
from apps.client import client
from apps.backups import backups

# the users control class.
class Manager(object):
	def __init__(self):

		# objects.
		self.client = client.client
		self.backups = backups.backups
	
		# service.	
		Files.chmod(f"{SOURCE}/__defaults__/start", permission="+x")
		self.service = dev0s.system.Service(
			id="vbackups",
			user=dev0s.defaults.vars.user,
			group=None,
			start=[f"{SOURCE}/__defaults__/start"],
			description="VBackups Web Interface",
			restart=True,
			restart_limit=5,
			restart_delay=10,
			logs=Files.join(DATABASE, "logs/logs"),
			errors=Files.join(DATABASE, "logs/errors"),
			traceback="dev0s.system.Service", )
		response = self.service.check()
		if not response.success: response.crash(json=dev0s.defaults.options.json)
		
		#

	# encryption.
	def install_encryption(self, passphrase=None, verify_passphrase=None, interactive=False):

		# generate.
		response = ssht00ls_agent.generate(
			passphrase=passphrase, 
			verify_passphrase=verify_passphrase,
			interactive=interactive,)
		if not response.success: return response

		# check client.
		response = self.client.initialize()
		if not response.success: return response
		
		# response.
		return dev0s.response.success("Successfully installed and activated the encryption.", log_level=0)

		#
	def activate_encryption(self, passphrase=None, interactive=False):
		
		# activate.
		response = ssht00ls_agent.activate(
			passphrase=passphrase, 
			interactive=interactive)
		if not response.success: return response

		# check client.
		response = self.client.initialize()
		if not response.success: return response

		# response.
		return dev0s.response.success("Successfully activated the encryption.", log_level=0)
		
		#

	# properties.
	@property
	def installed(self):
		return self.__installed__()
	def __installed__(self, filter=None, options=["django", "database", "client", "settings", "encryption"]):
		if filter == None:
			for i in options:
				b = self.__installed__(filter=i)
				if dev0s.defaults.options.log_level >= 3: print(f"@installed {i}: {b}")
				if not b:
					return False
			return True
		elif filter == "django":
			return website.users.exists(username=ADMINISTRATOR, filter="django")
		elif filter == "database":
			return Files.exists(DATABASE.join("data/db.sqlite3"))
		elif filter == "client":
			return Files.exists(DATABASE.join(f"clients/{ADMINISTRATOR}/private_key")) and Files.exists(DATABASE.join(f"clients/{ADMINISTRATOR}/public_key")) and self.client.client.alias in ssht00ls.clients
		elif filter == "settings":
			return None not in [ self.client.settings["server"]["name"], self.client.settings["server"]["domain"] ]
		elif filter == "encryption":
			return ssht00ls_agent.generated
		else: raise ValueError(f"Invalid usage, filter [{filter}] is not a valid option, options: {Array(options).string(joiner=' ')}.")
	
	#

# initialized classes.
manager = Manager()

