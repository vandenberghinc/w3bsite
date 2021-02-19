#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the apps holder.
class TemplateData(syst3m.objects.Object):
	def __init__(self, data={}):
		# defaults.
		syst3m.objects.Object.__init__(self)
		