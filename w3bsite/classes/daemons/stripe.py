#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the stripe subscription daemon.
# used for verifying subscriptions.
class SubscriptionVerification(syst3m.objects.Thread):
	def __init__(self, 
		# the daemons sleep time.
		sleeptime=60,
		# the website.users object,.
		users=None,
		# the website.stripe object.
		stripe=None, 
	):
		
		# defaults.
		syst3m.objects.Thread.__init__(self, log_level=0)
		self.assign(defaults.dict())

		# arguments.
		self.sleeptime = sleeptime

		# objects.
		self.users = users
		self.stripe = stripe

		#
	def __run__(self):
		while self.running:
			if self.should_stop(): break
			time.sleep(self.sleeptime)
	def verify(self,
		# the users email.
		email=None,
		# the users api key.
		api_key=None,
	):
		a=1
		