#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes.utils import utils
import shutil, math, time

# the system control class.
class Metrics(object):
	def __init__(self, database=None):

		# docs.
		DOCS = {
			"module":"website.metrics", 
			"initialized":True,
			"description":[], 
			"chapter": "Website", }

		# history.
		self.history = 7 # in days.

		# attributes.
		self.database = database
		if isinstance(self.database, (str,String,FilePath)):
			self.database = Directory(str(self.database))

		# files.
		if not Files.exists(self.database.join("data/metrics")): Files.create(self.database.join("data/metrics"), directory=True)
		self.__requests__ = Dictionary(path=self.database.join("data/metrics/requests", ""), load=True, default={})
		self.__saving_requests__ = False

		# clean.
		self.clean()

		#
	def clean(self):


		# cleanings.
		date = Date()
		decreased = date.decrease(date.timestamp, days=self.history)
		for id, requests in self.__requests__.items():
			for timestamp in list(requests.keys()):
				if date.compare(timestamp, decreased) in ["past"]:
					del self.__requests__[id][str(timestamp)]

		# save cleaned.
		self.__requests__.save()

		# handler.
		return dev0s.response.success("Successfully cleaned the metrics data.")

		#

	# metrics functions.
	def requests(self):
		
		# get historical data.
		self.__safe_load__(self.__requests__)
		items = []
		for request_id in ["web", "api", "auth"]:
			try: self.__requests__[request_id]
			except KeyError: self.__requests__[request_id] = {}
			for key, value in self.__requests__[request_id].items():
				if key not in items: items.append(key)
		d = {}
		for timestamp in items:
			l = {}
			for request_id in ["web", "api", "auth"]:
				try: l[request_id] = self.__requests__[request_id][timestamp]
				except KeyError: l[request_id] = {}
			d[timestamp] = {
				"Web Requests":len(l["web"]),
				"API Requests":len(l["api"]),
				"Auth Requests":len(l["auth"]),
			}
		
		# graph data.
		graph = self.create_line_graph(
			data=d, 
			keep=["Web Requests", "API Requests", "Auth Requests"], 
			colors={
				"Web Requests":"#FD304E",
				"API Requests":"#323B83",
				"Auth Requests":"#006633",
			},
		)

		# handler.
		return dev0s.response.success("Successfully retrieved the requests data.", {
			"data":d,
			"graph":graph,
		})
	def auth_requests(self):
		
		# get historical data.
		self.__safe_load__(self.__requests__)
		d = {}
		try: self.__requests__["auth"]
		except KeyError: self.__requests__["auth"] = {}
		for timestamp, data in self.__requests__["auth"].items():
			success, failed = 0, 0 
			for item in data:
				if item["response"]["success"]: success += 1
				else: failed += 1
			d[timestamp] = {
				"Successfull":success,
				"Failed":failed,
			}
		
		# graph data.
		graph = self.create_line_graph(
			data=d, 
			keep=["Successfull", "Failed", "Auth Requests"], 
			colors={
				"Successfull":"#FD304E",
				"Failed":"#323B83",
			},
		)

		# handler.
		return dev0s.response.success("Successfully retrieved the auth requests data.", {
			"data":d,
			"graph":graph,
		})
	def disk_space(self, mode="GB"):
		def auto_size(size_bytes):
			if size_bytes == 0:
				return "0B"
			size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
			i = int(math.floor(math.log(size_bytes, 1024)))
			p = math.pow(1024, i)
			s = round(size_bytes / p, 2)
			return "%s %s" % (s, size_name[i])
		def size(size_bytes):
			if mode.upper() == "TB":
				return int(('{:,}'.format(int(round(size_bytes/1024**4,2))).replace(',', '.')).replace(".",""))
			elif mode.upper() == "GB":
				return int(('{:,}'.format(int(round(size_bytes/1024**3,2))).replace(',', '.')).replace(".",""))
			elif mode.upper() == "MB":
				return int(('{:,}'.format(int(round(size_bytes/1024**2,2))).replace(',', '.')).replace(".",""))
			elif mode.upper() == "KB":
				return int(('{:,}'.format(int(round(size_bytes/1024,2))).replace(',', '.')).replace(".",""))
			else:
				return int(('{:,}'.format(int(int(size_bytes))).replace(',', '.')).replace(".",""))
		total, used, free = shutil.disk_usage(str(self.database))
		return dev0s.response.success("Successfully retrieved the free disk space.", {
			"total":size(total), 
			"used":size(used), 
			"free":size(free),
			"graph":self.create_pie_graph(
				data={
					"Used (GB)":size(used),
					"Free (GB)":size(free),
				},
				colors={
					"Used (GB)": "#FD304E",
					"Free (GB)": "#323B8390",
				},
			),
		})
	
	# create graph function.
	def create_pie_graph(self, 
		# the data.
		data={
			"Used (GB)":15,
			"Free (GB)":3,
		},
		# the key's colors.
		colors={
			"Used (GB)": "#FD304E",
			"Free (GB)": "#323B8390",
		},
		# the keys to keep.
		keep=["*"],
		# fill background color.
		fill=False,
	):
		labels, new_data, background, border = [], [], [], []
		for key,value in data.items():
			if "*" in keep or key in keep:
				labels.append(key)
				new_data.append(value)
				background.append(colors[key])
				border.append(colors[key]+"90")
		return {
			"labels": labels,
			"datasets": [
				{
			        "data": new_data,
			        "backgroundColor":background,
			        "borderColor":border,
			        "fill": fill,
			    }
			],
		}
	def create_line_graph(self, 
		# the data.
		data={
			"$timestamp":{
				"active":10,
				"non_active":3,
			},
		}, 
		# the key's colors.
		colors={
			"active":"#323B83",
			"non_active":"#FD304E",
		},
		# the keys to keep.
		keep=["*"], 
		# fill background color.
		fill=False,
	):
		summed = {}
		for key, value in data.items():
			for _key_, _value_ in value.items():
				if "*" in keep or _key_ in keep:
					try:summed[_key_]
					except KeyError: summed[_key_] = []
					summed[_key_].append(_value_)
		datasets = []
		for key, value in summed.items():
			datasets.append({
				"label": key[0].upper() + key[1:],
				"backgroundColor": colors[key],
				"borderColor": colors[key]+"90",
				"fill": fill,
				"data": value
			})
		return {
			"labels": list(data.keys()),
			"datasets": datasets,
		}

	# count requests.
	def count_api_request(self, request, data={}):
		return self.count_request(request, id="api", save=random.randrange(0, 101) <= 10, data=data)
	def count_web_request(self, request, data={}):
		return self.count_request(request, id="web", save=random.randrange(0, 101) <= 10, data=data)
	def count_auth_request(self, request, data={}):
		return self.count_request(request, id="auth", save=True, data=data)
	def count_request(self, request, id=None, data={"url":None}, save=False):
		if id == None: raise dev0s.exceptions.InvalidUsage("Define parameter: id.")
		try: username = request.user.username
		except: username = None
		date = Date()
		timestamp = f"{date.timestamp[:-2]}{int(int(date.minute)/10)}0"
		self.__safe_load__(self.__requests__)
		try:self.__requests__[str(id)]
		except KeyError: self.__requests__[str(id)] = {}
		try:self.__requests__[str(id)][timestamp]
		except KeyError: self.__requests__[str(id)][timestamp] = []
		l_data = {
			"username":username,
			"ip":utils.get_client_ip(request), }
		for key,value in data.items(): l_data[key] = value
		self.__requests__[id][timestamp].append(l_data)
		if save and not self.__saving_requests__:
			self.__saving_requests__ = True
			self.__requests__.save()
			self.__saving_requests__ = False
		return dev0s.response.success(f"Successfully counted request [{id}].")

	# system functions.
	def __safe_load__(self, dict_object, reattempt=True):
		try:
			dict_object.load()
		except: 
			dict_object.dictionary = {}
			dict_object.save() 
	
	
#