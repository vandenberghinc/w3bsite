
# imports.
from classes.config import *
from classes import utils


# hello world.
class HelloWorld(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, 
			# the views id (required).
			id="hello-world", 
			# the base path (required; if url path is null).
			base="requests/",
		)
	def view(self, request):
		#if ..:
		#	return self.error("Error: ...")
		return self.success("Success ...", {"hello":"world"})

# hello world compact.
class HelloWorldSmall(w3bsite.views.Request):
	def __init__(self):
		w3bsite.views.Request.__init__(self, "requests/compact/", "hello-world")
	def view(self, request):
		return self.success("Success ...", {"hello":"world"})

# the activate requests.
urlpatterns = w3bsite.views.build_urls([
	#HelloWorld(),
	#HelloWorldSmall(),
])