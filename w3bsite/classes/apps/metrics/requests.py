
# classes imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# the authentication requests.
class Requests(_defaults_.Defaults):
	def __init__(self, 
		# passed Website.x objects.
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# urlpatterns.
		if dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
			self.urls = []
		else:
			self.urls = views.build_urls([
				self.Requests(defaults=defaults),
				self.AuthRequests(defaults=defaults),
				self.DiskSpace(defaults=defaults),
			])

	# get requests metrics.
	class Requests(views.Request):
		def __init__(self, defaults=None):
			views.Request.__init__(self, "requests/metrics/", "requests", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check signed in.
			if dev0s.system.env.get("METRICS_AUTH_REQUIRED", format=bool, default=True):
				response = self.website.users.authenticated(request)
				if not response.success: return response
				elif request.user.username not in ["administrator"]:
					return self.permission_denied(request)

			# make request.
			return self.response(self.website.metrics.requests())

			#

	# get auth requests metrics.
	class AuthRequests(views.Request):
		def __init__(self, defaults=None):
			views.Request.__init__(self, "requests/metrics/", "auth_requests", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check signed in.
			if dev0s.system.env.get("METRICS_AUTH_REQUIRED", format=bool, default=True):
				response = self.website.users.authenticated(request)
				if not response.success: return response
				elif request.user.username not in ["administrator"]:
					return self.permission_denied(request)

			# make request.
			return self.response(self.website.metrics.auth_requests())
			
			#

	# get disk space.
	class DiskSpace(views.Request):
		def __init__(self, defaults=None):
			views.Request.__init__(self, "requests/metrics/", "disk_space", website=defaults.website)
			self.assign(defaults.dict())
		def request(self, request):

			# check signed in.
			if dev0s.system.env.get("METRICS_AUTH_REQUIRED", format=bool, default=True):
				response = self.website.users.authenticated(request)
				if not response.success: return response
				elif request.user.username not in ["administrator"]:
					return self.permission_denied(request)

			# make request.
			return self.response(self.website.metrics.disk_space())
		
		#

#