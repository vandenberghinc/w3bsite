
# imports.
from classes.config import *

# app settings.
APP_NAME = Formats.FilePath(Formats.FilePath(__file__).base()).name()

# the .. view.
class home():
	def view(request):
		return render(request, APP_NAME+"/home.html", TEMPLATE_DATA)
