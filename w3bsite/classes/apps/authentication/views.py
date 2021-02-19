#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# the x views.
class Views(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())
		
		# urlpatterns.
		self.urls = views.build_urls([
			self.SignIn(defaults=defaults),
			self.SignUp(defaults=defaults),
			self.Reset(defaults=defaults),
			self.Activate(defaults=defaults),
		])

	# sign in.
	class SignIn(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "authentication/", "signin", template_data=self.template_data, html=f"w3bsite/classes/apps/authentication/html/signin.html")
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	# sign up.
	class SignUp(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "authentication/", "signup", template_data=self.template_data, html=f"w3bsite/classes/apps/authentication/html/signup.html")
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	# reset password.
	class Reset(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "authentication/", "reset", template_data=self.template_data, html=f"w3bsite/classes/apps/authentication/html/reset.html")
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	# activate account.
	class Activate(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "authentication/", "activate", template_data=self.template_data, html=f"w3bsite/classes/apps/authentication/html/activate.html")
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)