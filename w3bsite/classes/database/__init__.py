#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the database class.
class Database(object):
	def __init__(self, firestore=None, path=None):
		self.firestore = firestore
		self.path = gfp.clean(path)
		self.file_path = self.fp = FilePath(self.path)
		if not self.fp.exists():
			r3sponse.log(f"&ORANGE&Root permission&END& required to create database [{self.path}].")
			os.system(f"sudo mkdir {self.path}")
			Files.chmod(path=self.path, permission=700, sudo=True)
			Files.chown(path=self.path, owner=syst3m.defaults.vars.user, group=syst3m.defaults.vars.group, sudo=True)
		self.cache = None
		if self.firestore != None:
			self.cache = syst3m.cache.Cache(path=self.path)
	def load(self, path=None, format="str"):
		if self.firestore != None:
			return self.firestore.load(reference)
		elif self.cache != None:
			return self.cache.load(group=reference, format=format)
	def save(self, path=None, data=None, format="str"):
		if self.firestore != None:
			return self.firestore.load(reference, data)
		elif self.cache != None:
			return self.cache.save(group=reference, data=data, format=format)
	def delete(self, path=None, data=None, format="str"):
		if self.firestore != None:
			return self.firestore.delete(reference)
		elif self.cache != None:
			return self.cache.delete(group=reference)
	# str representation.
	def __str__(self):
		return str(self.fp.path)
	
			