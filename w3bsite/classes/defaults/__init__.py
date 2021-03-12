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
		if dictionary.__class__.__name__ in ["Dictionary"]:
			dictionary = dictionary.dictionary
		elif dictionary.__class__.__name__ in ["ResponseObject", "OutputObject"]:
			dictionary = dictionary.dict()
		if dictionary.__class__.__name__ in ["Dictionary"]:
			l_template_data = dict(self.template_data.dictionary)
		else:
			l_template_data = dict(self.template_data)
		dictionary = Dictionary(l_template_data) + Dictionary(dictionary)
		if dictionary.__class__.__name__ in ["Dictionary"]: dictionary = dictionary.dictionary
		return dictionary
		#

	