#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# app.
APP = "authentication"

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
		if dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
			self.urls = []
		else:
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
			views.View.__init__(self, f"{APP}/", "signin", html=f"w3bsite/classes/apps/authentication/html/signin.html", website=defaults.website)
			self.assign(defaults.dict())
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	# sign up.
	class SignUp(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			views.View.__init__(self, f"{APP}/", "signup", html=f"w3bsite/classes/apps/authentication/html/signup.html", website=defaults.website)
			self.assign(defaults.dict())
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	# reset password.
	class Reset(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			views.View.__init__(self, f"{APP}/", "reset", html=f"w3bsite/classes/apps/authentication/html/reset.html", website=defaults.website)
			self.assign(defaults.dict())
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	# activate account.
	class Activate(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			views.View.__init__(self, f"{APP}/", "activate", html=f"w3bsite/classes/apps/authentication/html/activate.html", website=defaults.website)
			self.assign(defaults.dict())
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	