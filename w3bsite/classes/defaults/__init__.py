#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the website defaults object class.
class Defaults(Object):
	def __init__(self, attributes={}, traceback="w3bsite.Website.defaults",):

		# object defaults.
		Object.__init__(self, traceback=traceback)
		self.assign(attributes)

		#
	def template(self, dictionary={}):
		dictionary = Dictionary(self.template_data) + Dictionary(dictionary)
		if isinstance(dictionary, Dictionary): dictionary = dictionary.dictionary
		return dictionary
		#

	