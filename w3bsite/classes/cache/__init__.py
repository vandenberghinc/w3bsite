#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils

# the users class.
class Cache(object):
	def __init__(self):	

		# variables.
		self.__cache__ = {}
		
		#
	def set(self, 
		# the cache mode (example: subscriptions) (optional).
		mode=None, 
		# the cache key (example: someuser@gmail.com) (required).
		key=None, 
		# the cached value.
		value=None,
		# the minutes before reset (leave None to use no refresh).
		reset=60*24,
	):
		data = {
			"value":value,
			"reset":reset,
			"timestamp":Formats.Date().timestamp,
		}
		if mode != None:
			try:self._cache_[mode]
			except KeyError: self.__cache__[mode] = {}
			self.__cache__[mode][key] = data
		else:
			self.__cache__[key] = data
		return r3sponse.success_response(f"Successfully cached [{mode}.{key}].") 
	def get(self, 
		# the cache mode (example: subscriptions) (optional).
		mode=None, 
		# the value key (example: someuser@gmail.com) (required).
		key=None, 
	):
		if mode != None:
			try:self.__cache__[mode]
			except KeyError:  return r3sponse.error_response(f"No cached {mode} data available.") 
			try:data = self.__cache__[mode][key]
			except KeyError:  return r3sponse.error_response(f"No cached {mode}.{key} data available.") 
		else:
			try:data = self.__cache__[key]
			except KeyError:  return r3sponse.error_response(f"No cached {key} data available.") 
		if isinstance(data["reset"], int):
			date = Formats.Date()
			increased = date.increase(data["timestamp"], minutes=data["reset"])
			if date.compare(increased, date.timestamp) in ["past", "present"]:
				return r3sponse.error_response(f"Cache refresh required for {mode}.{key}.") 
		return r3sponse.success_response(f"Successfully retrieved cache [{mode}.{key}].", {
			"value":data["value"],
		}) 