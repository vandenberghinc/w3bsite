#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils, views
from w3bsite.classes import defaults as _defaults_

# the payments requests.
class Requests(_defaults_.Defaults):
	def __init__(self,
		# passed Website.x objects.
		stripe=None,
		defaults=None,
	):
		# defaults.
		_defaults_.Defaults.__init__(self)
		defaults.stripe = stripe
		self.assign(defaults.dict())
		
		# urlpatterns.
		if dev0s.system.env.get("MIGRATIONS", format=bool, default=False):
			self.urls = []
		else:
			self.urls = views.build_urls([
				self.Subscriptions.Purchase(defaults=defaults),
				self.Subscriptions.Create(defaults=defaults),
				self.Subscriptions.Delete(defaults=defaults),
				self.Subscriptions.List(defaults=defaults),
				self.Methods.Create(defaults=defaults),
				self.Methods.Delete(defaults=defaults),
				self.Methods.List(defaults=defaults),
			])

	# the subscriptions.
	class Subscriptions:

		# all-in-one purchase request.
		class Purchase(views.Request):
			def __init__(self, defaults=None,):
				views.Request.__init__(self, "requests/payments/subscriptions/", "purchase", website=defaults.website)
				_defaults_.Defaults.__init__(self)
				self.assign(defaults.dict())
			def request(self, request):

				# check overall rate limit.
				response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
				if not response.success: return self.response(response)

				# check authenticated.
				response = self.users.authenticated(request)
				if not response.success: return self.response(response)
				email = response.email
				try: api_key = response.api_key
				except: api_key = None

				# get parameters.
				parameters, response = self.parameters.get(request, [
					"product",
					"plan",
					"card_name",
					"card_number",
					"card_expiration_month",
					"card_expiration_year",
					"card_cvc",])
				if not response.success: return self.response(response)

				# request.
				return self.response(self.users.create_subscription(
					email=email,
					api_key=api_key,
					product=parameters["product"],
					plan=parameters["plan"],
					card_name=parameters["card_name"],
					card_number=parameters["card_number"],
					card_cvc=parameters["card_cvc"],
					card_expiration_month=parameters["card_expiration_month"],
					card_expiration_year=parameters["card_expiration_year"],))

		# create subscription.
		class Create(views.Request):
			def __init__(self, defaults=None,):
				views.Request.__init__(self, "requests/payments/subscriptions/", "create", website=defaults.website)
				_defaults_.Defaults.__init__(self)
				self.assign(defaults.dict())
			def request(self, request):

				# check overall rate limit.
				response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
				if not response.success: return self.response(response)

				# check authenticated.
				response = self.users.authenticated(request)
				if not response.success: return self.response(response)
				email = response.email
				try: api_key = response.api_key
				except: api_key = None

				# get parameters.
				parameters, response = self.parameters.get(request, [
					"product",
					"plan",])
				if not response.success: return self.response(response)

				# request.
				return self.response(self.users.create_subscription(
					email=email,
					api_key=api_key,
					product=parameters["product"],
					plan=parameters["plan"],
					))

		# delete subscription.
		class Delete(views.Request):
			def __init__(self, defaults=None,):
				views.Request.__init__(self, "requests/payments/subscriptions/", "delete", website=defaults.website)
				_defaults_.Defaults.__init__(self)
				self.assign(defaults.dict())
			def request(self, request):

				# check overall rate limit.
				response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
				if not response.success: return self.response(response)

				# check authenticated.
				response = self.users.authenticated(request)
				if not response.success: return self.response(response)
				email = response.email

				###################
				# by subscription id.

				# get parameters.
				parameters, response = self.parameters.get(request, [
					"subscription_id",])
				if response.success: 

					# request.
					return self.response(self.stripe.subscriptions.cancel(
						email=email,
						subscription_id=parameters["subscription_id"],))

				###################
				# by plan & product.
				else:

					# get parameters.
					parameters, response = self.parameters.get(request, [
						"product",
						"plan",])
					if not response.success: return self.response(response)

					# convert plan.
					response = self.stripe.get_plan_id(product=parameters["product"], plan=parameters["plan"])
					if not response.success: return self.response(response)
					plan_id = response.id

					# request.
					return self.response(self.stripe.subscriptions.cancel(
						email=email,
						plan=plan_id,))

		# list methods.
		class List(views.Request):
			def __init__(self, defaults=None,):
				views.Request.__init__(self, "requests/payments/subscriptions/", "list", website=defaults.website)
				_defaults_.Defaults.__init__(self)
				self.assign(defaults.dict())
			def request(self, request):

				# check overall rate limit.
				response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
				if not response.success: return self.response(response)

				# check authenticated.
				response = self.users.authenticated(request)
				if not response.success: return self.response(response)
				email = response.email

				# get customer id.
				response = self.stripe.customers.get_id(email=email)
				if not response.success: return self.response(response)
				customer_id = response.id

				# list.
				response = self.stripe.subscriptions.get(email=email, active_only=True)
				if not response.success: return self.response(response)
				subscriptions = response.subscriptions
				for plan_id in list(subscriptions.keys()):
					response = self.stripe.get_product_id_by_plan_id(plan_id)
					if not response.success: return self.response(response)
					product_id = response.id
					response = self.stripe.get_product_name(product_id)
					if not response.success: return self.response(response)
					product = response.name
					response = self.stripe.get_plan_name(plan_id)
					if not response.success: return self.response(response)
					plan = response.name
					subscriptions[plan_id]["product"] = product
					subscriptions[plan_id]["plan"] = plan
					subscriptions[plan_id]["favicon"] = self.stripe.template_data["PRODUCTS"][product][plan]["favicon"]
					subscriptions[plan_id]["price"] = self.stripe.template_data["PRODUCTS"][product][plan]["price"]

				# request.
				return self.success(f"Successfully listed {len(subscriptions)} active subscription(s).", {
					"subscriptions":subscriptions,
				})

	# the payment methods.
	class Methods:

		# create method.
		class Create(views.Request):
			def __init__(self, defaults=None,):
				views.Request.__init__(self, "requests/payments/methods/", "create", website=defaults.website)
				_defaults_.Defaults.__init__(self)
				self.assign(defaults.dict())
			def request(self, request):

				# check overall rate limit.
				response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
				if not response.success: return self.response(response)

				# check authenticated.
				response = self.users.authenticated(request)
				if not response.success: return self.response(response)
				email = response.email

				# get parameters.
				parameters, response = self.parameters.get(request, [
					"number",
					"month",
					"year",
					"cvc",])
				if not response.success: return self.response(response)

				# get customer id.
				response = self.stripe.customers.get_id(email=email)
				if not response.success: return self.response(response)
				customer_id = response.id

				# request.
				return self.response(self.stripe.customers.create_card(
					id=customer_id,
					number=parameters["number"],
					month=parameters["month"],
					year=parameters["year"],
					cvc=parameters["cvc"],))

		# delete method.
		class Delete(views.Request):
			def __init__(self, defaults=None,):
				views.Request.__init__(self, "requests/payments/methods/", "delete", website=defaults.website)
				_defaults_.Defaults.__init__(self)
				self.assign(defaults.dict())
			def request(self, request):

				# check overall rate limit.
				response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
				if not response.success: return self.response(response)

				# check authenticated.
				response = self.users.authenticated(request)
				if not response.success: return self.response(response)
				email = response.email

				# get customer id.
				response = self.stripe.customers.get_id(email=email)
				if not response.success: return self.response(response)
				customer_id = response.id

				# request.
				return self.response(self.stripe.customers.delete_card(
					id=customer_id,
					))

		# list methods.
		class List(views.Request):
			def __init__(self, defaults=None,):
				views.Request.__init__(self, "requests/payments/methods/", "list", website=defaults.website)
				_defaults_.Defaults.__init__(self)
				self.assign(defaults.dict())
			def request(self, request):

				# check overall rate limit.
				response = self.rate_limit.verify(ip=utils.get_client_ip(request), mode="daily", limit=1000, reset_minutes=3600*24, increment=True)
				if not response.success: return self.response(response)

				# check authenticated.
				response = self.users.authenticated(request)
				if not response.success: return self.response(response)
				email = response.email

				# get customer id.
				response = self.stripe.customers.get_id(email=email)
				if not response.success: return self.response(response)
				customer_id = response.id

				# request.
				return self.response(self.stripe.customers.get_cards(
					id=customer_id,))
