#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the website defaults object class.
class Defaults(syst3m.objects.Object):
	def __init__(self,
		# info.
		root=None,
		version=None,
		library=None,
		database=None,
		name=None,
		domain=None,
		https_domain=None,
		author=None,
		email=None,
		country_code=None,
		province=None,
		city=None,
		organization=None,
		organization_unit=None,
		developers=None,
		remote=None,
		live=None,
		interactive=None,
		_2fa=None,
		maintenance=False,
		# objects.
		template_data=None,
		aes=None,
		cache=None,
		logging=None,
	):

		# object defaults.
		syst3m.objects.Object.__init__(self)

		# defaults.
		self.root = root
		self.version = version
		self.library = library
		self.database = database
		self.name = name
		self.author = author
		self.email = email
		self.organization = organization
		self.country_code = country_code
		self.domain = domain
		self.https_domain = https_domain
		self.developers = developers
		self.remote = remote
		self.live = live
		self.interactive = interactive
		self.province = province
		self.city = city
		self.organization_unit = organization_unit
		self._2fa = _2fa
		self._maintenance_ = maintenance

		# objects.
		self.template_data = template_data
		self.aes = aes
		self.cache = cache
		self.logging = logging

		#
	