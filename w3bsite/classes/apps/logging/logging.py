#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes.utils import utils
import shutil, math, time

# the system control class.
class Logging(Object):
	def __init__(self, attributes={}):

		# docs.
		DOCS = {
			"module":"website.logging", 
			"initialized":True,
			"description":[], 
			"chapter": "Logging", }

		# defaults.
		Object.__init__(self)
		self.assign(attributes)
		
		# attributes.
		if isinstance(self.database, (str,String,FilePath)):
			self.database = Directory(str(self.database))

		# objects.
		self.alerts = self.Alerts(attributes=self.dict())

		#

	# copied functions.
	def log(self, 
		# option 1:
		# the message (#1 param).
		message=None,
		# option 2:
		# the error.
		error=None,
		# option 3:
		# the response dict (leave message None to use).
		response={},
		# print the response as json.
		json=False,
		# optionals:
		# the active log level.
		log_level=0,
		# the required log level for when printed to console (leave None to use self.log_level).
		required_log_level=None, 
		# save to log file.
		save=False,
		# save errors always (for options 2 & 3 only).
		save_errors=None,
		# the log mode (leave None for default).
		mode=None,
	):
		return dev0s.response.log(
			message=message,
			error=error,
			response=response,
			json=json,
			log_level=log_level,
			required_log_level=required_log_level,
			save=save,
			save_errors=save_errors,
			mode=mode,)
	def load_logs(self, format="webserver", options=["webserver", "cli", "array", "string"]):
		return dev0s.response.load_logs(format=format)
		#
	def reset_logs(self, format="webserver", options=["webserver", "cli", "array", "string"]):
		return dev0s.response.reset_logs(format=format)
		#
		
		#
	def log_to_file(self, message, raw=False):
		return dev0s.response.log_to_file(message, raw=raw)
		#

	# the alerts object class.
	class Alerts(Object):
		def __init__(self, attributes={}):

			# docs.
			DOCS = {
				"module":"website.logging.alerts", 
				"initialized":True,
				"description":[], 
				"chapter": "Logging", }

			# defaults.
			Object.__init__(self)
			self.assign(attributes)

			# check dir.
			if self.live:
				if not Files.exists(self.database.join("logs")): 
					Files.create(self.database.join("logs"), directory=True)

			# attributes.
			if self.live:
				self.alerts = Dictionary({}, path=self.database.join("logs/alerts"), default={})
			else:
				self.alerts = Dictionary({}, path=self.database.join("logs/alerts"))

			#

		# save an alert.
		def save(self, 
			# the alert's id (str).
			id="testalert",
			# the alert's title (str).
			title="Warning!", 
			# the alert's message (str). 
			message="Some message.",
			# the alert's right button redirect url (str).  
			redirect="/dashboard/home/", 
			# the alert's right button redirect text (str).  
			redirect_button="Ok", 
			# the alert's icon path.  
			icon="/media/icons/warning.png",
			# the urls on which the alert will be shown (list) (use [*] for all urls).
			urls=["*"],
			# the users to which the alert will be shown (list) (use [*] for all users).
			users=["*"],
		):
			try: alerts = self.alerts.load()
			except: alerts = {}
			try: alerts[id]
			except: alerts[id] = {}
			if Files.exists(self.database.join("logs/alerts")):
				size = gfp.size(path=self.database.join("logs/alerts"), mode="mb", format="integer")
				if size >= 25: 
					alerts = {id:{}}
			alerts[id][Date().seconds_timestamp] = {
				"title":title,
				"message":message,
				"redirect":redirect,
				"redirect_button":redirect_button,
				"icon":icon,
				"timestamp":Date().seconds_timestamp,
				"urls":urls,
				"users":users,
				"read":False,
			}
			self.alerts.dictionary = alerts
			self.alerts.save()
			#

		# check alerts.
		def check(self,
			# specific alert id's (str, list) (optional).
			id=None,
			# the active user (str) (optional).
			username=None,
			# the active url (str) (optional).
			url=None,
		):	
			# checks.
			if isinstance(id, (str, String)):
				id = [id]

			# iterate.
			for _id_, alerts in self.alerts.items():
				for timestamp, _alert_ in alerts.items():
					if not alert["read"]:
						if (
							(id == None or _id_ in id) 
							and 
							(username == None or username in alert["users"]) 
							and 
							(url == None or url in alert["urls"])
						):
							return dev0s.response.success("Successfully checked the alerts.", {
								"alert":alert,
							})
			return dev0s.response.success("Successfully checked the alerts.", {
				"alert":None,
			})


		# mark a alert as read.
		def mark(self, 
			# the alert's id.
			id=None, 
			# the alert's timestamp.
			timestamp=None,
		):
			self.alerts.load()
			try:
				self.alerts[id][timestamp]['read'] = True
			except: 
				self.logging.log(f"Failed to mark alert {id} {timestamp}, alert [{id}] does not exist.")
				return None
			self.alerts.save()
			#

		#
	
	#	
#	
	
#
