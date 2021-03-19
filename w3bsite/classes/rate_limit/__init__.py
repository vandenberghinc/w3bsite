
# imports.
from w3bsite.classes.config import *
from w3bsite.classes import defaults as _defaults_

# the rate limit object class.
class RateLimit(_defaults_.Defaults):
	def __init__(self, 
		# objects.
		db=None,
		# defaults.
		defaults=None,
	):	

		# docs.
		DOCS = {
			"module":"website.ratelimit", 
			"initialized":True,
			"description":[
				"The <attribute>website.ratelimit</attribute> object class.",
				"Used for managing the request limits.",
			], 
			"chapter": "Website", }

		# defaults.
		_defaults_.Defaults.__init__(self, traceback="w3bsite.Website.ratelimit",)
		self.assign(defaults.dict())

		# objects.
		self.db = db

		#
	def increment(self, 
		# user identification options (select one option):
		#	option 1: user email.
		email=None, 
		username=None,
		#	option 2: the requests ip.
		ip=None, 
		# rate lmit mode id.
		mode=None, 
		# the increment count.
		count=1,
	):
		
		# check options.
		if email == None and ip == None: return dev0s.response.error("Specify parameter [email] or [ip].")
		response = dev0s.response.parameters.check(
			traceback=self.__traceback__(function="increment"),
			parameters={
				"mode":mode,
			})
		if not response.success: return response

		# by email.
		reference = None
		if email != None or username != None:
			reference = self.__get_path__(username=username, email=email,)

		# by ip.
		elif ip != None:
			reference = f"ips/{ip}"

		# load.
		response = self.db.load(reference)
		if not response.success: 
			if "does not exist" in response.error or "No such file or directory" in response.error:
				response["data"] = {}
			else:
				return response
		document = response["data"]
		try:
			rate_limits = document["rate_limits"]
		except KeyError:
			rate_limits = {}
		except TypeError:
			document = {}
			rate_limits = {}

		# check.
		date = Date()
		try: rate_limits[mode]
		except KeyError: rate_limits[mode] = {}
		try: rate_limits[mode]["timestamp"]
		except KeyError: rate_limits[mode]["timestamp"] = date.timestamp
		try: rate_limits[mode]["rate"]
		except KeyError: rate_limits[mode]["rate"] = 0
		
		# increment.
		rate_limits[mode]["rate"] += count
		
		# save.
		document["rate_limits"] = rate_limits
		response = self.db.save(reference, document)
		if not response.success: return response
		return dev0s.response.success("Successfully incremented the rate limit.")

		#
	def verify(self, 
		# user identification options (select one option):
		#	option 1: user email.
		email=None, 
		username=None,
		#	option 2: the requests ip.
		ip=None, 
		# rate lmit mode id.
		mode=None, 
		# rate limit.
		limit=1000,
		# reset after. 
		reset_minutes=3600*24, 
		# increment on succes.
		increment=False, 
		increment_count=1,
	):
		# check options.
		if email == None and ip == None: return dev0s.response.error("Specify parameter [email] or [ip].")
		response = dev0s.response.parameters.check(
			traceback=self.__traceback__(function="verify"),
			parameters={
				"mode":mode,
			})
		if not response.success: return response

		# by email.
		reference = None
		if email != None or username != None:
			reference = self.__get_path__(username=username, email=email)

		# by ip.
		elif ip != None:
			reference = f"ips/{ip}"

		# check reset timestamp.
		response = self.db.load(reference)
		if not response.success: 
			if "does not exist" in response.error or "No such file or directory" in response.error:
				response["data"] = {}
			else:
				return response
		document = response["data"]
		try:
			rate_limits = document["rate_limits"]
		except KeyError:
			rate_limits = {}
		except TypeError:
			document = {}
			rate_limits = {}

		# check.
		date = Date()
		try: rate_limits[mode]
		except KeyError: rate_limits[mode] = {}
		try: rate_limits[mode]["timestamp"]
		except KeyError: rate_limits[mode]["timestamp"] = date.timestamp
		try: rate_limits[mode]["rate"]
		except KeyError: rate_limits[mode]["rate"] = 0
		timestamp = rate_limits[mode]["timestamp"]
		increased = Date(date.increase(timestamp, format=date.timestamp_format, minutes=reset_minutes))
		if date >= increased:
			rate_limits[mode]["rate"] = 0
			rate_limits[mode]["timestamp"] = date.timestamp
			document["rate_limits"] = rate_limits
			response = self.db.save(reference, document)
			if not response.success: return response

		# check rate.
		if rate_limits[mode]["rate"] < limit:
			if increment:
				rate_limits[mode]["rate"] += increment_count
				document["rate_limits"] = rate_limits
				response = self.db.save(reference, document)
				if not response.success: return response
			return dev0s.response.success(f"Successfully verified the {mode} rate limit.")
		else:
			return dev0s.response.error(f"You have exhausted your {mode} rate limit.")
	def __get_path__(self, email=None, username=None):
		if self.id_by_username:
			if username == None and email != None:
				response = self.get(email=email)
				if not response.success: response.crash()
				username = response.user.username
			id = username
		else:
			if email == None and username != None:
				response = self.get(username=username)
				if not response.success: response.crash()
				email = response.user.email
			id = email
		if self.db.mode == "cache" and Files.exists(f"{self.database}/{self.users_subpath}/{id}/settings"):
			path = f"{self.users_subpath}/{id}/settings"
		else:
			path = f"{self.users_subpath}/{id}"
		return path

		
