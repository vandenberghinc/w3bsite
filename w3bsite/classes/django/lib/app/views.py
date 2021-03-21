
# imports.
from classes.config import *

# home.
class Home(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, 
			# the views id (required).
			id="home",
			# the base path (required; if url path is null).
			base="dashboard/",
			# the template data (required).
			template_data=website.template_data,
			# the landing page.
			landing_page=True,
		)
	def view(self, request):
		try:
			
			# return render.
			return self.render(request, self.template_data+{})

		# catch error.
		except Exception as e: return self._500(request, error=e)

		#

# compact.
class HelloWorld(w3bsite.views.View):
	def __init__(self):
		w3bsite.views.View.__init__(self, "dashboard/" "hello-world", template_data=website.template_data)
	def view(self, request):
		try:

			# return render.
			return self.render(request, self.template_data+{})

		# catch error.
		except Exception as e: return self._500(request, error=e)

		#
		
# the active views.
urlpatterns = w3bsite.views.build_urls([
	#Home(),
	#HelloWorld(),
])