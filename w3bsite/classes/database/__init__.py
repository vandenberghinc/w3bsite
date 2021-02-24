#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the database class.
class Database(object):
	def __init__(self, firestore=None, path=None):
		self.firestore = firestore
		self.path = path
		self.cache = None
		if self.path != None:
			self.path = gfp.clean(self.path)
			self.cache = syst3m.cache.Cache(path=self.path)
	def load(self, path=None, format="str"):
		if self.firestore != None:
			return self.firebase.firestore.load(reference)
		elif self.cache != None:
			return self.cache.load(group=reference, format=format)
	def save(self, path=None, data=None, format="str"):
		if self.firestore != None:
			return self.firebase.firestore.load(reference, data)
		elif self.cache != None:
			return self.cache.save(group=reference, data=data, format=format)
	def delete(self, path=None, data=None, format="str"):
		if self.firestore != None:
			return self.firebase.firestore.delete(reference)
		elif self.cache != None:
			return self.cache.delete(group=reference)
	
			