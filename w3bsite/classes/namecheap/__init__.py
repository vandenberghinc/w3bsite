#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_

# the namecheap object class.
class Namecheap(_defaults_.Defaults):
	# source: https://www.namecheap.com/support/api/methods/
	# go to [Profile > Tools > Developer > API > Manage] and enable the APi and whitelist your public ip.
	def __init__(self,
		# your namecheap username.
		username=None,
		# your namecheap api key.
		api_key=None,
		# sandbox boolean (does not seem to work namecheap end).
		sandbox=False,
		# defaults.
		defaults=None,
	):	

		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# check arguments.
		#response = r3sponse.check_parameters({
		#	#"ip":ip,
		#})
		#if not response.success: raise ValueError(response.error)

		# arguments.
		self.username = username
		self.api_key = api_key

		# pre domain.
		self.pre_domain, splitted = "", self.domain.split(".")
		if len(splitted) > 2:
			c, stop = 0, len(splitted)-1
			for i in splitted:
				c += 1
				if c == stop: break
				if self.pre_domain == "": self.pre_domain = i
				else: self.pre_domain += "."+i
		self.post_domain = self.domain.replace(f"{self.pre_domain}.", "")

		# get public ip.
		self.public_ip = NETWORK_INFO["public_ip"]

		# set api base url.
		if sandbox:
			self.base_url = f"https://api.sandbox.namecheap.com/xml.response?ApiUser={self.username}&ApiKey={self.api_key}&UserName={self.username}&ClientIp={self.public_ip}"
		else:
			self.base_url = f"https://api.namecheap.com/xml.response?ApiUser={self.username}&ApiKey={self.api_key}&UserName={self.username}&ClientIp={self.public_ip}"
		
		# set tld & sld.
		self.sld, self.tld = None, None
		if self.domain != None:
			response = self.get_sld_and_tld(self.domain)
			if response.error != None: raise ValueError(response['error'])
			self.sld, self.tld = response["sld"], response["tld"]

		#
	def check_domain(self, domain=None):

		# set default domain.
		if domain == None: domain = self.domain

		# get domains.
		response = self.get_domains()
		if response.error != None: return response
		try:
			info = response["domains"][domain]
			exists = True
		except: exists = False
		return r3sponse.success_response(f"Successfully checked the ownership for domain [{domain}] from namecheap user [{self.username}].", {"exists":exists})

		#
	def get_domains(self):

		# api request.
		response = self.__request__("namecheap.domains.getList")
		if response["api_response"]["errors"] != None: 
			try: error = response["api_response"]["errors"]["error"]["#text"]
			except KeyError: error = response["api_response"]["errors"]
			return r3sponse.error_response(f"Failed to retrieve the domains of namecheap user [{self.username}], error: {error}")

		# handle response.
		domains = {}
		try: result = response["api_response"]["command_response"]["domain_get_list_result"]
		except KeyError: result = {}
		for key, domain in result.items():
			if isinstance(domain, dict):
				domains[domain["name"]] = domain
			elif isinstance(domain, list):
				for item in domain:
					item = self.__serialize_dictionary__(item)
					domains[item["name"]] = item
			else: raise ValueError(f"Unkown domain type: {domain}.")

		# handlers.
		return r3sponse.success_response(f"Successfully retrieved the domains of namecheap user [{self.username}].", {
			"domains":domains,
		})

		#
	def get_info(self, domain=None):

		# set default domain.
		if domain == None: domain = self.domain

		# check domain.
		response = self.check_domain(domain)
		if response.error != None: return response
		elif not response["exists"]:
			return r3sponse.error_response(f"Namecheap user [{self.username}] does not own domain [{domain}].")

		# api request get info.
		response = self.__request__("namecheap.domains.getInfo", {"DomainName":domain})
		if response["api_response"]["errors"] != None: 
			try: error = response["api_response"]["errors"]["error"]["#text"]
			except KeyError: error = response["api_response"]["errors"]
			return r3sponse.error_response(f"Failed to retrieve the info of domain [{domain}] from namecheap user [{self.username}], error: {error}")

		# handle response.
		try:
			info = response["api_response"]["command_response"]["domain_get_info_result"]
		except KeyError:
			return r3sponse.error_response(f"Failed to retrieve the info of domain [{domain}] from namecheap user [{self.username}].")

		# handlers.
		return r3sponse.success_response(f"Successfully retrieved the domain info of namecheap user [{self.username}].", {
			"info":info,
		})

		#
	def get_dns(self, domain=None):

		# set default domain.
		if domain == None: domain = self.domain

		# check domain.
		response = self.check_domain(domain)
		if response.error != None: return response
		elif not response["exists"]:
			return r3sponse.error_response(f"Namecheap user [{self.username}] does not own domain [{domain}].")

		# api request.
		response = self.get_sld_and_tld(domain)
		if response.error != None: raise ValueError(response['error'])
		sld, tld = response["sld"], response["tld"]
		response = self.__request__("namecheap.domains.dns.getHosts", {"SLD":sld, "TLD":tld})
		if response["api_response"]["errors"] != None: 
			try: error = response["api_response"]["errors"]["error"]["#text"]
			except KeyError: error = response["api_response"]["errors"]
			return r3sponse.error_response(f"Failed to retrieve the dns info for domain [{domain}] from namecheap user [{self.username}], error: {error}")

		# handle response.
		try:
			data = response["api_response"]["command_response"]["domain_dnsget_hosts_result"]
		except KeyError:
			return r3sponse.error_response(f"Failed to retrieve the dns info for domain [{domain}] from namecheap user [{self.username}].")

		# iterate data.
		records = {}
		if isinstance(data["host"], dict):
			serialized = self.__serialize_dictionary__(data["host"])
			if serialized['address'][len(serialized['address'])-1] == ".": serialized['address'] = serialized['address'][:-1]
			tag = self.tag_dns(
				# the dns record type,
				type=serialized['type'],
				# the dns record host,
				host=serialized['name'],
				# the dns record value/address,
				value=serialized['address'],)["tag"]
			old_id, new_id = "name", 'host' ; i = serialized[old_id] ; del serialized[old_id] ; serialized[new_id] = i
			old_id, new_id = "address", 'value' ; i = serialized[old_id] ; del serialized[old_id] ; serialized[new_id] = i
			records[tag] = serialized
		elif isinstance(data["host"], list):
			for item in data["host"]:
				serialized = self.__serialize_dictionary__(item)
				if serialized['address'][len(serialized['address'])-1] == ".": serialized['address'] = serialized['address'][:-1]
				tag = self.tag_dns(
					# the dns record type,
					type=serialized['type'],
					# the dns record host,
					host=serialized['name'],
					# the dns record value/address,
					value=serialized['address'],)["tag"]
				old_id, new_id = "name", 'host' ; i = serialized[old_id] ; del serialized[old_id] ; serialized[new_id] = i
				old_id, new_id = "address", 'value' ; i = serialized[old_id] ; del serialized[old_id] ; serialized[new_id] = i
				records[tag] = serialized

		# handlers.
		return r3sponse.success_response(f"Successfully retrieved the dns info of namecheap user [{self.username}].", {
			"records":records,
		})

		#
	def check_dns(self,
		# the domain (optional).
		domain=None,
		# the dns record type,
		type=None,
		# the dns record host,
		host=None,
		# the dns record value/address,
		value=None,
		# the get_dns.records dictionary (optionally to increase speed).
		records=None,
	):
		
		# set default domain.
		if domain == None: domain = self.domain

		# get tag.
		tag = self.tag_dns(
			# the dns record type,
			type=type,
			# the dns record host,
			host=host,
			# the dns record value/address,
			value=value,)["tag"]

		# get dns.
		if records == None:
			response = self.get_dns(domain=domain)
			if response.error != None: return response
			records = response["records"]

		# handlers.
		exists = tag in list(records.keys())
		return r3sponse.success_response(f"Successfully checked dns record [{tag}] of namecheap user [{self.username}].", {
			"exists":exists,
			"tag":tag,
		})

		#
	def set_dns(self,
		# the domain (optional).
		domain=None,
		# the dns records (erases all others).
		records={
			"$record-1":{
				# the dns record type (required),
				"type":None,
				# the dns record host (required),
				"host":None,
				# the dns record value/address (required),
				"value":None,
				# the dns record ttl (optional default is 1800),
				"ttl":1800,
			},
		},
	):
		
		# set default domain.
		if domain == None: domain = self.domain

		# check domain.
		response = self.check_domain(domain)
		if response.error != None: return response
		elif not response["exists"]:
			return r3sponse.error_response(f"Namecheap user [{self.username}] does not own domain [{domain}].")

		# sld & tld.
		response = self.get_sld_and_tld(domain)
		if response.error != None: raise ValueError(response['error'])
		sld, tld = response["sld"], response["tld"]

		# api request.
		data, c = {
			"SLD":sld, 
			"TLD":tld,
		}, 0
		for tag,info in records.items():
			try:
				data[f"HostName{c}"] = info["host"]
				data[f"RecordType{c}"] = info["type"]
				data[f"Address{c}"] = info["value"]
				try:
					data[f"TTL{c}"] = info["ttl"]
				except KeyError:
					data[f"TTL{c}"] = 1800
			except KeyError:
				return r3sponse.error_response(f"Invalid usage, each record dictionary must have the following keys: [host, type, value].")
			c += 1
		response = self.__request__("namecheap.domains.dns.setHosts", data)
		if response["api_response"]["errors"] != None: 
			try: error = response["api_response"]["errors"]["error"]["#text"]
			except KeyError: error = response["api_response"]["errors"]
			return r3sponse.error_response(f"Failed to set the dns records for domain [{domain}] from namecheap user [{self.username}], error: {error}")

		# handle response.
		try:
			success = response["api_response"]["command_response"]["domain_dnsset_hosts_result"]["is_success"] == True
		except KeyError:
			success = False

		# handlers.
		if success:
			return r3sponse.success_response(f"Successfully set dns records for domain [{domain}] from namecheap user [{self.username}].")
		else:
			return r3sponse.error_response(f"Failed to set the dns records for domain [{domain}] from namecheap user [{self.username}].")

		#
	def add_dns(self,
		# the domain (optional).
		domain=None,
		# the dns record type,
		type=None,
		# the dns record host,
		host=None,
		# the dns record value/address,
		value=None,
		# the dns record ttl (optional default is 1800),
		ttl=1800,
		# the get_dns.records dictionary (optionally to increase speed).
		records=None,
	):

		# get dns records.
		if records == None:
			response = self.get_dns(domain)
			if response.error != None: return response
			records = response["records"]

		# check heroku dns records.
		response = self.check_dns(
			domain=domain,
			type=type,
			host=host,
			value=value,
			records=records,)

		# handle error.
		if response.error != None:  return response

		# handle exact duplicate.
		elif response["exists"]:
			tag = response["tag"]
			return r3sponse.error_response(f"DNS record [{tag}] from namecheap domain [{domain}] already exists.")

		# add new.
		else:
			
			# add dns records.
			tag = response["tag"]
			records[tag] = {
				"type":type,
				"host":host,
				"value":value,
				"ttl":ttl,
			}
			print(f"Adding DNS record [{type} {host} {value}] ...")
			response = self.set_dns(
				domain=domain,
				records=records,)
			if response.error != None: return response

			# success.
			return r3sponse.success_response(f"Successfully added dns record [{tag}] to namecheap domain [{domain}].", {"tag":tag})

		#
	def tag_dns(self,
		# the dns record type,
		type=None,
		# the dns record host,
		host=None,
		# the dns record value/address,
		value=None,
	):
		tag = f"{type}|{host}|{value}"
		return r3sponse.success_response(f"Successfully taggeed dns record [{tag}].", {"tag":tag})
	def get_sld_and_tld(self, domain=None):

		# set default domain.
		if domain == None: domain = self.domain

		# get sld & tld.
		sld, tld = "", ""
		b = domain.split('.')
		c, m, = 0, len(b)
		for i in b:
			if c < m-1:
				if sld == "":
					sld = str(i)
				else: 
					sld += '.'+i
			else:
				tld = str(i)
			c += 1

		# handlers.
		return r3sponse.success_response(f"Successfully retrieded the SLD & TLD of domain [{domain}].", {
			"tld":tld,
			"sld":sld,
		})
		
		#
	def get_tls(self):

		# api request.
		response = self.__request__("namecheap.ssl.getList", {})
		if response["api_response"]["errors"] != None: 
			try: error = response["api_response"]["errors"]["error"]["#text"]
			except KeyError: error = response["api_response"]["errors"]
			return r3sponse.error_response(f"Failed to retrieve the tls list from namecheap user [{self.username}], error: {error}")

		# handle response.
		try:
			data = response["api_response"]["command_response"]["ssllist_result"]
		except KeyError:
			return r3sponse.error_response(f"Failed to retrieve the tls list from namecheap user [{self.username}].")

		# iterate data.
		tls = {}
		if data == None:
			a=1 # keep empty.
		elif isinstance(data["ssl"], dict):
			tls[data["ssl"]["certificate_id"]] = data["ssl"]
		elif isinstance(data["ssl"], list):
			for _data_ in data["ssl"]:
				_data_ = self.__serialize_dictionary__(_data_)
				tls[_data_["certificate_id"]] = _data_

		# handlers.
		return r3sponse.success_response(f"Successfully retrieved the tls list for namecheap user [{self.username}].", {
			"tls":tls,
			"certificates":len(tls),
		})

		#
	def create_tls(self,
		# the expiration years.
		years=2,
		# the tls type.
		type="PositiveSSL",
	):

		# api request.
		response = self.__request__("namecheap.ssl.create", {
			"Years":years,
			"Type":type,
		})
		if response["api_response"]["errors"] != None: 
			try: error = response["api_response"]["errors"]["error"]["#text"]
			except KeyError: error = response["api_response"]["errors"]
			return r3sponse.error_response(f"Failed to create tls certificate from namecheap user [{self.username}], error: {error}")

		# handle response.
		try:
			data = response["api_response"]["command_response"]["sslcreate_result"]
		except KeyError:
			return r3sponse.error_response(f"Failed to create a tls certificate for namecheap user [{self.username}].")

		# handlers.
		if data["is_success"]:
			return r3sponse.success_response(f"Successfully created a tls certificate for namecheap user [{self.username}].", {
				"certificate_id":data["sslcertificate"]["certificate_id"],
				"order_id":data["order_id"],
				"transaction_id":data["transaction_id"],
				"charged_amount":data["charged_amount"],
				"status":data["sslcertificate"]["status"],
				"type":data["sslcertificate"]["ssltype"],
				"years":data["sslcertificate"]["years"],
			})
		else:
			return r3sponse.error_response(f"Failed to create a tls certificate for namecheap user [{self.username}].")

		#
	def activate_tls(self,
		# the certificate's id.
		certificate_id=None,
	):

		# check csr.
		csr = f"{self.root}/.secrets/tls/server.csr"
		if not os.path.exists(csr):
			return r3sponse.error_response(f"There is no tls certificate present.")
		csr = utils.__load_file__(csr)

		# api request.
		response = self.__request__("namecheap.ssl.activate", {
			"CertificateID":certificate_id,
			"AdminEmailAddress":self.email,
			"CSR":csr,
			"DNSDCValidation":"true",
		})
		if response["api_response"]["errors"] != None: 
			try: error = response["api_response"]["errors"]["error"]["#text"]
			except KeyError: error = response["api_response"]["errors"]
			return r3sponse.error_response(f"Failed to activate tls certificate [{certificate_id}] from namecheap user [{self.username}], error: {error}")

		# handle response.
		try:
			data = response["api_response"]["command_response"]["sslactivate_result"]
		except KeyError:
			return r3sponse.error_response(f"Failed to retrieve the tls list from namecheap user [{self.username}].")

		# handlers.
		if not data["is_success"]:
			return r3sponse.error_response(f"Failed to activate tls certificate [{certificate_id}] from namecheap user [{self.username}].")

		# add dns validation record. 
		dns_validation = data["dnsdcvalidation"]["dns"]
		response = self.add_dns(
			# the domain (optional).
			domain=self.post_domain,
			# the dns record type,
			type="CNAME",
			# the dns record host,
			host=dns_validation["host_name"].split(".")[0]+self.pre_domain,
			# the dns record value/address,
			value=dns_validation["target"],
			# the get_dns.dns dictionary (optionally to increase speed).
			records=None,)
		if response.error != None and "] already exists." not in response.error: return response
		
		# handlers.
		return r3sponse.success_response(f"Successfully activated tls certificate [{certificate_id}] from namecheap user [{self.username}].")

		#
	# system functions.
	def __request__(self, command="namecheap.domains.getList", data={}):
		if data == {}:
			url = f"{self.base_url}&command={command}"
		else:
			url = f"{self.base_url}&command={command}&{urllib.parse.urlencode(data)}"
		response = requests.get(url)
		return self.__serialize_dictionary__(utils.__xml_to_json__(response.text))
	def __serialize_string__(self, string, banned_characters=["@"]):
		c, s, l = 0, "", False
		for char in string:
			if char not in banned_characters:
				# regular letter.
				if char.lower() == char:
					s += char.lower()
					l = False
				# capital letter.
				else:
					if c == 0:
						s += char.lower()
					else:
						if l:
							s += char.lower()
						else:
							s += "_"+char.lower()
					l = True
				c += 1
		return s
	def __serialize_dictionary__(self, response):
		_response_ = {}
		for key,value in response.items():
			s_key = self.__serialize_string__(key)
			if isinstance(value, dict):
				_response_[s_key] = self.__serialize_dictionary__(value)
			elif isinstance(value, str):
				try: integer = int(value)
				except: integer = False
				if integer != False:
					_response_[s_key] = integer
				elif value in ["false", "False", "FALSE", "DISABLED"]:
					_response_[s_key] = False
				elif value in ["true", "True", "TRUE", "ENABLED"]:
					_response_[s_key] = True
				else:
					_response_[s_key] = value
			else:
				_response_[s_key] = value
		return _response_



