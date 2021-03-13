#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the users class.
class Logging(object):
	def __init__(self, name=None, root=None, database=None):

		# docs.
		DOCS = {
			"module":"website.logging", 
			"initialized":True,
			"description":[], }

		# attributes.
		self.name = name
		self.root = root
		self.database = database
		self.log_file = f"{self.root}/logs/logs"
		#if not Files.exists(f"{self.database}/logs"):
		#	Files.create(f"{self.database}/logs", directory=True)

	# log to logfile.
	def log(self,
		# option 1.
		# 	the message response body.
		message=None,
		# option 2.
		# 	the error response body.
		error=None,
		# option 3.
		# 	the entire response.
		response=None,
	):
		# get options.
		msg = None
		if message != None:
			msg = message
		elif error != None:
			msg = "Error: "+error
		elif response != None:
			if response.success:
				msg = response["message"]
			else:
				msg = "Error: "+response.error

		# log to file.
		__log__(msg)

		#

	# system functions.
	def __log__(self, string):
		msg = f"{Date().seconds_timestamp}: {string}"
		print(msg)
		with open(self.log_file, "a") as file:
			file.write(msg)

	#