#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import exceptions

# the database class.
class Database(syst3m.objects.Traceback):
	def __init__(self, firestore=None, path=None):
		
		# traceback.
		syst3m.objects.Traceback.__init__(self, traceback="w3bsite.Website.database")

		# checks.
		if firestore == None and path == None: raise exceptions.InvalidUsage(self.__traceback__()+" Both parameters firestore & path are None.")

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
		if self.firestore == None:
			self.cache = syst3m.cache.Cache(path=self.path)

		#
	def load(self, path=None, format="str"):
		if path == None: return r3sponse.error(self.__traceback__(function="load")+" Define parameter: [path].")
		if self.firestore != None:
			return self.firestore.load(path)
		elif self.cache != None:
			return self.cache.load(group=path, format=format)
		else: raise exceptions.InvalidUsage(self.__traceback__(function="load")+" Both parameters firestore & path are None.")
	def save(self, path=None, data=None, format="str"):
		if path == None: return r3sponse.error(self.__traceback__(function="save")+" Define parameter: [path].")
		if data == None: return r3sponse.error(self.__traceback__(function="save")+" Define parameter: [data].")
		if self.firestore != None:
			return self.firestore.save(path, data)
		elif self.cache != None:
			try:
				self.cache.save(group=path, data=data, format=format)
			except Exception as e: return r3sponse.error(str(e))
			return r3sponse.success(f"Successfully saved [{path}].")
		else: raise exceptions.InvalidUsage(self.__traceback__(function="save")+" Both parameters firestore & path are None.")
	def delete(self, path=None, data=None, format="str"):
		if path == None: return r3sponse.error(self.__traceback__(function="delete")+" Define parameter: [path].")
		if self.firestore != None:
			return self.firestore.delete(path)
		elif self.cache != None:
			return self.cache.delete(group=path)
		else: raise exceptions.InvalidUsage(self.__traceback__(function="delete")+" Both parameters firestore & path are None.")
	# str representation.
	def __str__(self):
		return str(self.fp.path)
	
			