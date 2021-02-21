
# imports.
from classes.config import *

# app settings.
APP_NAME = FilePath(FilePath(__file__).base()).name()

# the .. view.
class my_view():
	def view(request):
		return render(request, APP_NAME+"/my_view.html", TEMPLATE_DATA)
