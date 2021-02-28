#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the database class.
class Database(syst3m.objects.Traceback):
	def __init__(self, firestore=None, path=None):
		
		# traceback.
		syst3m.objects.Traceback.__init__(self, traceback="w3bsite.Website.database")

		# attributes.
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

		#
	def load(self, path=None, format="str"):
		if path == None: return r3sponse.error(self.__traceback__(function="load")+" Define parameter: [path].")
		if self.firestore != None:
			return self.firestore.load(path)
		elif self.cache != None:
			return self.cache.load(group=path, format=format)
	def save(self, path=None, data=None, format="str"):
		if path == None: return r3sponse.error(self.__traceback__(function="save")+" Define parameter: [path].")
		if self.firestore != None:
			return self.firestore.save(path, data)
		elif self.cache != None:
			return self.cache.save(group=path, data=data, format=format)
	def delete(self, path=None, data=None, format="str"):
		if path == None: return r3sponse.error(self.__traceback__(function="delete")+" Define parameter: [path].")
		if self.firestore != None:
			return self.firestore.delete(path)
		elif self.cache != None:
			return self.cache.delete(group=path)
	# str representation.
	def __str__(self):
		return str(self.fp.path)
	
			