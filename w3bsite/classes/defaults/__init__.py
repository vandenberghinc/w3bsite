#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes.utils import utils

# the website defaults object class.
class Defaults(Object):
	def __init__(self, attributes={}, traceback="w3bsite.Website.defaults",):

		# object defaults.
		Object.__init__(self, traceback=traceback)
		self.assign(attributes)

		#
	def template(self, dictionary={}):
		return utils.template(old=self.template_data, new=dictionary)
		#

	