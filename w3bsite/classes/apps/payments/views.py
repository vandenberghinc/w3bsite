#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# the payments views.
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
			self.Purchase(defaults=defaults),
			self.Cancel(defaults=defaults),
		])

	# purchase.
	class Purchase(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "payments/", "purchase", template_data=self.template_data, html=f"w3bsite/classes/apps/payments/html/purchase.html")
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)

	# cancel.
	class Cancel(views.View):
		def __init__(self, defaults=None):
			_defaults_.Defaults.__init__(self)
			self.assign(defaults.dict())
			views.View.__init__(self, "payments/", "cancel", template_data=self.template_data, html=f"w3bsite/classes/apps/payments/html/cancel.html")
		def view(self, request):
			if self._maintenance_: return self.maintenance(request)
			return self.render(request)
