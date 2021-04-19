#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import exceptions

# the database class.
class Database(Traceback):
	def __init__(self, firestore=None, path=None, live=False):
		
		# docs.
		DOCS = {
			"module":"website.db", 
			"initialized":True,
			"description":[], 
			"chapter": "Database", }

		# traceback.
		Traceback.__init__(self, traceback="w3bsite.Website.db")

		# checks.
		if firestore == None and path == None: raise exceptions.InvalidUsage(self.__traceback__()+" Both parameters firestore & path are None.")

		# attributes.
		self.mode = "firestore"
		self.live = live
		self.firestore = firestore
		self.path = gfp.clean(path)
		self.file_path = self.fp = FilePath(self.path)
		if firestore == None:
			self.database = dev0s.database.Database(self.path)
			self.mode = "cache"
			if self.live and not self.fp.exists():
				dev0s.response.log(f"&ORANGE&Root permission&END& required to create database [{self.path}].")
				os.system(f"sudo mkdir {self.path}")
				Files.chmod(path=self.path, permission=700, sudo=True)
				Files.chown(path=self.path, owner=dev0s.defaults.vars.user, group=dev0s.defaults.vars.group, sudo=True)

		#

	# functions.
	def load(self, path=None):
		if path == None: return dev0s.response.error(self.__traceback__(function="load")+" Define parameter: [path].")
		path = gfp.clean(path)
		if self.mode == "firestore":
			return self.firestore.load(path)
		elif self.mode == "cache":
			return self.database.load(path=path)
		else: raise exceptions.InvalidUsage(self.__traceback__(function="load")+f" Unknown mode [{self.mode}].")
	def save(self, path=None, data=None, overwrite=False):
		if path == None: return dev0s.response.error(self.__traceback__(function="save")+" Define parameter: [path].")
		if data == None: return dev0s.response.error(self.__traceback__(function="save")+" Define parameter: [data].")
		path = gfp.clean(path)
		if self.mode == "firestore":
			if isinstance(data, (dict, Dictionary)):
				response = self.load(path=path)
				if response.success:
					return self.firestore.save(path, Dictionary(response.data).insert(data))
				else:
					return self.firestore.save(path, data)
			else:
				return self.firestore.save(path, data)
		elif self.mode == "cache":
			return self.database.save(path=path, data=data, overwrite=overwrite)
		else: raise exceptions.InvalidUsage(self.__traceback__(function="save")+f" Unknown mode [{self.mode}].")
	def delete(self, path=None):
		if path == None: return dev0s.response.error(self.__traceback__(function="delete")+" Define parameter: [path].")
		path = gfp.clean(path)
		if self.mode == "firestore":
			return self.firestore.delete(path)
		elif self.mode == "cache":
			return self.database.delete(path=path)
		else: raise exceptions.InvalidUsage(self.__traceback__(function="delete")+f" Unknown mode [{self.mode}].")

	# get names.
	def names(self,
		# the sub path (leave None to use the root path)
		path=None,
	):

		# checks.
		if path == None: return dev0s.response.error(self.__traceback__(function="names")+" Define parameter: [path].")
		path = gfp.clean(path)

		# vars.
		names = []

		# firestore.
		if self.mode == "firestore":
			response = self.firestore.load_collection(path)
			if not response.success: response.crash()
			names = response["collection"]

		# cache.
		elif self.mode == "cache":
			return self.database.names(path=path)

		# handler.
		return names

		#

	# path functions.
	def subpath(self, fullpath):
		return self.file_path.clean(path=fullpath.replace(self.path, ""), remove_double_slash=True)
	def fullpath(self, subpath):
		return self.file_path.clean(path=f"{self.path}/{subpath}", remove_double_slash=True)
	def join(self, name=None, type=""):
		return self.file_path.join(name, type)
		#
		
	# representation.
	def __str__(self):
		return str(self.fp.path)
	def __repr__(self):
		return str(self)

	#

	
			
