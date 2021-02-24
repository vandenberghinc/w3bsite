
# imports.
from w3bsite.classes.config import *
from w3bsite.classes import defaults as _defaults_

# the rate limit object class.
class RateLimit(_defaults_.Defaults):
	def __init__(self, 
		# objects.
		database=None,
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
		
		# objects.
		self.database = database

		#
	def increment(self, 
		# user identification options (select one option):
		#	option 1: user email.
		email=None, 
		#	option 2: the requests ip.
		ip=None, 
		# rate lmit mode id.
		mode=None, 
		# the increment count.
		count=1,
	):
		
		# check options.
		if email == None and ip == None: return r3sponse.error("Specify parameter [email] or [ip].")
		response = r3sponse.check_parameters({
			"mode":mode,})
		if not response.success: return response

		# by email.
		reference = None
		if email != None:
			reference = f"users/{email}"

		# by ip.
		elif ip != None:
			reference = f"ips/{ip}"

		# load.
		response = self.database.load(reference, format="json")
		if not response.success: 
			if ip != None and "Document " in response.error and " does not exist" in response.error:
				response["document"] = {}
			else:
				return response
		document = response["document"]
		try:
			rate_limits = document["rate_limits"]
		except KeyError:
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
		response = self.database.save(reference, document, format="json")
		if not response.success: return response
		return r3sponse.success("Successfully incremented the rate limit.")

		#
	def verify(self, 
		# user identification options (select one option):
		#	option 1: user email.
		email=None, 
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
		if email == None and ip == None: return r3sponse.error("Specify parameter [email] or [ip].")
		response = r3sponse.check_parameters({
			"mode":mode,})
		if not response.success: return response

		# by email.
		reference = None
		if email != None:
			reference = f"users/{email}"

		# by ip.
		elif ip != None:
			reference = f"ips/{ip}"

		# check reset timestamp.
		response = self.database.load(reference, format="json")
		if not response.success: 
			if ip != None and "Document " in response.error and " does not exist" in response.error:
				response["document"] = {}
			else:
				return response
		document = response["document"]
		try:
			rate_limits = document["rate_limits"]
		except KeyError:
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
		increased = date.increase(timestamp, format=date.timestamp_format, minutes=reset_minutes)
		comparison = date.compare(comparison=date.timestamp, current=increased, format=date.timestamp_format)
		if comparison in ["future", "present"]:
			rate_limits[mode]["rate"] = 0
			rate_limits[mode]["timestamp"] = date.timestamp
			document["rate_limits"] = rate_limits
			response = self.database.save(reference, document, format="json")
			if not response.success: return response

		# check rate.
		if rate_limits[mode]["rate"] < limit:
			if increment:
				rate_limits[mode]["rate"] += increment_count
				document["rate_limits"] = rate_limits
				response = self.database.save(reference, document, format="json")
				if not response.success: return response
			return r3sponse.success(f"Successfully verified the {mode} rate limit.")
		else:
			return r3sponse.error(f"You have exhausted your {mode} rate limit.")

		
