#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_
from w3bsite.classes.apps import payments, authentication, template_data

# the apps holder.
class Apps(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		rate_limit=None,
		users=None,
		stripe=None,
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		defaults.rate_limit = rate_limit
		defaults.users = users
		self.assign(defaults.dict())

		# apps.
		self.authentication = self.Authentication(defaults=defaults)
		self.payments = self.Payments(defaults=defaults, stripe=stripe)

	# the authentication app.
	class Authentication(_defaults_.Defaults):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			self.requests = authentication.requests.Requests(defaults=defaults,)
			self.views = authentication.views.Views(defaults=defaults,)

	# the payments app.
	class Payments(_defaults_.Defaults):
		def __init__(self, defaults=None, stripe=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			self.requests = payments.requests.Requests(defaults=defaults, stripe=stripe)
			self.views = payments.views.Views(defaults=defaults)


