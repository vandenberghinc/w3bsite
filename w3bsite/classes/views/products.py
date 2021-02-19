
# imports
from w3bsite.classes.views.defaults import *

# the products overview.
class Products(View):
	def __init__(self, 
		# the base path (required; if url path is null) [#1 argument].
		base=None,
		# the views id (required) [#2 argument].
		id=None, 
		# the url path (optional).
		url=None,
		# the html path (optional).
		html=None,
		# enable if this view is the [/] landing page.
		landing_page=False,
		# the template data (required).
		template_data={},
		# the w3bsite.Website object.
		website=None,
	):
		# defaults.
		View.__init__(self,
			base=base,
			id=id,
			url=url,
			html=html,
			landing_page=landing_page,
			template_data=template_data,
			# the view type.
			type="DocumentationView",)
		self.website = website
	def view(self, request):
		return self.render(request, self.template_data, html=f"{SOURCE_PATH}/classes/views/html/products.hml")


# the product view.
class Product(View):
	def __init__(self, 
		# the base path (required; if url path is null) [#1 argument].
		base=None,
		# the views id (required) [#2 argument].
		id=None, 
		# the url path (optional).
		url=None,
		# the html path (optional).
		html=None,
		# enable if this view is the [/] landing page.
		landing_page=False,
		# the template data (required).
		template_data={},
		# the w3bsite.Website object.
		website=None,
	):
		# defaults.
		View.__init__(self,
			base=base,
			id=id,
			url=url,
			html=html,
			landing_page=landing_page,
			template_data=template_data,
			# the view type.
			type="DocumentationView",)
		self.website = website
	def view(self, request):
		return self.render(request, self.template_data, html=f"{SOURCE_PATH}/classes/views/html/product.hml")