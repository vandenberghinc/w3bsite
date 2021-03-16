#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_
from w3bsite.classes.apps import payments, authentication, logging, metrics

# django imports.
from django.shortcuts import render

# the apps holder.
class Apps(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		template_data=None,
		rate_limit=None,
		users=None,
		stripe=None,
		utils=None,
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		defaults.template_data = template_data
		defaults.rate_limit = rate_limit
		defaults.users = users
		defaults.utils = utils
		self.assign(defaults.dict())

		# apps.
		self.exceptions = self.Exceptions(defaults=defaults)
		self.logging = self.Logging(defaults=defaults)
		self.metrics = self.Metrics(defaults=defaults)
		self.authentication = self.Authentication(defaults=defaults)
		self.payments = self.Payments(defaults=defaults, stripe=stripe)

	# the exceptions app.
	class Exceptions(_defaults_.Defaults):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
		def _404(self, request, *args, **argv):
			return render(request, 'w3bsite/classes/apps/defaults/html/404.html', self.template(self.template_data))
		def _500(self, request, *args, **argv):
			return render(request, 'w3bsite/classes/apps/defaults/html/500.html', self.template(self.template_data))

	# the logging app.
	class Logging(_defaults_.Defaults):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			self.requests = logging.requests.Requests(defaults=defaults,)

	# the metrics app.
	class Metrics(_defaults_.Defaults):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			self.requests = metrics.requests.Requests(defaults=defaults,)
			#self.views = metrics.views.Views(defaults=defaults,)

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


