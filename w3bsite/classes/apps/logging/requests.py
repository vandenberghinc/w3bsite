#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# the logging requests.
class Requests(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# urlpatterns.
		if dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
			self.urls = []
		else:
			self.urls = views.build_urls([
				self.Load(defaults=defaults),
				self.Reset(defaults=defaults),
			])

	# load the logs.
	class Load(views.Request):
		def __init__(self, defaults=None):
			views.Request.__init__(self, "requests/logs/", "load", website=defaults.website)
			self.assign(defaults.dict())
		@views.method_decorator(views.login_required)
		def request(self, request):

			# check root permissions.
			response = self.users.authenticated(request)
			if not response.success: return response

			# check root permissions.
			response = self.users.root_permission(request)
			if not response.success: return response

			# make request.
			return dev0s.response.load_logs(format="webserver")

			#

	# reset logs.
	class Reset(views.Request):
		def __init__(self, defaults=None):
			views.Request.__init__(self, "requests/logs/", "reset", website=defaults.website)
			self.assign(defaults.dict())
		@views.method_decorator(views.login_required)
		def request(self, request):

			# check root permissions.
			response = self.users.authenticated(request)
			if not response.success: return response

			# check root permissions.
			response = self.users.root_permission(request)
			if not response.success: return response

			# make request.
			return dev0s.response.reset_logs(format="webserver")

			#

	#

#