#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import defaults as _defaults_

# pip imports.
import stripe

# univeral functions.
def __handle_stripe_exception__(exception):
	if "Request req_" in f"{exception}": return r3sponse.error_response(f"{exception}".split(": ")[1])
	else: return r3sponse.error_response(f"{exception}")

# the stripe object class.
class Stripe(_defaults_.Defaults):
	# privacy policy generator.
	# https://getterms.io/
	def __init__(self,
		# the stripe secret key.
		secret_key=None,
		# 	the stripe publishable key.
		publishable_key=None,
		# the default subscription plans.
		subscriptions=None,
		# the default products.
		products=None,
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
		self.secret_key = secret_key
		self.publishable_key = publishable_key
		self._products_ = products
		self._subscriptions_ = subscriptions

		# stripe.
		if not isinstance(secret_key, str):
			raise ValueError("Define the parameter [secret_key].")
		self.stripe = stripe
		self.stripe.api_key = secret_key
		self.sandbox = "sk_test_" in self.secret_key
		if self.sandbox: self.sandbox_txt = "sandbox"
		else: self.sandbox_txt = "live"

		# template data.
		self.template_data["STRIPE"]["SECRET_KEY"] = None
		self.template_data["STRIPE"]["PUBLISHABLE_KEY"] = self.publishable_key
		self.template_data["STRIPE"]["PRODUCTS"] = {}

		# defaults.
		self.stripe_defaults = self.Defaults(
			secret_key=self.secret_key,
			publishable_key=self.publishable_key,
			products=self._subscriptions_,
			domain=self.domain,
			stripe=self.stripe,
			logging=self.logging,)

		# objects.
		self.customers = self.Customers(defaults=self.stripe_defaults)
		self.subscriptions = self.Subscriptions(defaults=self.stripe_defaults, customers=self.customers)
		self.plans = self.Plans(defaults=self.stripe_defaults, subscriptions=self.subscriptions)
		self.products = self.Products(defaults=self.stripe_defaults, plans=self.plans)

		# system variabels.
		self.product_ids = {
			"$product":"$id",
		}
		self.plan_ids = {
			"$product": {
				"$plan":"$id",
			}
		} 

		# autocheck.
		response = self.check()
		if not response.success: raise ValueError(response.error)

		#
	
	# wide functions.
	def check(self):
		def handle(response):
			products = response["products"]
			product_names = []
			product_ids = {}
			plan_names = {}
			plan_ids = {}
			for product_id, product in products.items():
				product_names.append(product["name"])
				product_ids[product["name"]] = product_id
				plan_names[product["name"]] = []
				plan_ids[product["name"]] = {}
				for plan_id, plan in product["plans"].items():	
					plan_names[product["name"]].append(plan["nickname"])
					plan_ids[product["name"]][plan["nickname"]] = plan_id
			names = []
			for i in product_names: names.append(i)
			for _, info in plan_names.items(): 
				for i in info: names.append(i)
			for name in names:
				for i in [
					",",
				]:
					if i in name: raise ValueError(f"Forbidden character {i} in product/plan name {name}.")
			return products, product_names, product_ids, plan_names, plan_ids

		# retrieve live products & plans.
		response = self.products.get(get_plans=True)
		if not response.success: return response
		products, product_names, product_ids, plan_names, plan_ids = handle(response)
		self.product_ids, self.plan_ids = product_ids, plan_ids

		# check specified products & plans.
		edits = 0
		for product, plans in self._subscriptions_.items():
			
			# check product.
			if not product in product_names:
				if self.interactive:
					if syst3m.console.input(f"There is no stripe product named {product}. Do you want to create this stripe product? ({self.sandbox_txt})", yes_no=True):
						# create product.
						response = self.products.create(
							id=product,
							description=None,)
						r3sponse.log(response=response)
						edits += 1
						if not response.success: return response
					else:
						return r3sponse.error_response(f"Aborted.")
				else:
					return r3sponse.error_response(f"Stripe product {product} does not exist.")

			# iterate plans.
			for plan_name, plan_info in plans.items():

				# check plan info.
				try: plan_info["price"]
				except KeyError: return r3sponse.error_response(f"Invalid <Website.stripe_products> parameter. Stripe plan {plan_name} from product {product} does not contain a price value.")
				try: plan_info["currency"]
				except KeyError: return r3sponse.error_response(f"Invalid <Website.stripe_products> parameter. Stripe plan {plan_name} from product {product} does not contain a currency value.")

				# check plan.
				if product not in list(plan_names.keys()) or plan_name not in plan_names[product]:
					if self.interactive:
						if syst3m.console.input(f"There is no stripe plan named {plan_name} for product {product}. Do you want to create this stripe plan? ({self.sandbox_txt})", yes_no=True):
							# create product.
							response = self.plans.create(
								id=plan_name,
								product=product,
								price=plan_info["price"],
								currency=plan_info["currency"],)
							r3sponse.log(response=response)
							edits += 1
							if not response.success: return response
						else:
							return r3sponse.error_response(f"Aborted.")
					else:
						return r3sponse.error_response(f"Stripe product {product} does not exist.")

				# check plan price change.
				elif plan_info["price"] != products[product_ids[product]]["plans"][plan_ids[product][plan_name]]["price"]:
					# handle soon.
					return r3sponse.error_response(f'Price change in product {product} plan {plan_name}, previous price: {products[product_ids[product]]["plans"][plan_ids[product][plan_name]]["price"]}, new price: {plan_info["price"]}.')
				

		# add plan id to tempalte data.
		if edits > 0:
			response = self.products.get(get_plans=True)
			if not response.success: return response
			products, product_names, product_ids, plan_names, plan_ids = handle(response)
			self.product_ids, self.plan_ids = product_ids, plan_ids
		for product, plans in self._subscriptions_.items(): 
			self.template_data["STRIPE"]["PRODUCTS"][product] = {}
			for plan_name, plan_info in plans.items():
				try: plan_id = plan_ids[product][plan_name]
				except KeyError: return r3sponse.error_response(f"Unable to find the id from plan {plan_name} product {product}.")
				try: favicon = plan_info["favicon"]
				except KeyError: favicon = None
				self.template_data["STRIPE"]["PRODUCTS"][product][plan_name] = {
					"id":plan_id,
					"price":plan_info["price"],
					"currency":plan_info["currency"],
					"plan":plan_name,
					"product":product,
					"favicon":favicon,
				}

		# handler.
		return r3sponse.success_response(f"Successfully checked the stripe products & plans.")
	def get_product_id(self, product=None):
		try: plan_id = self.product_ids[product]
		except KeyError: return r3sponse.error_response(f"Unable to find the id from product {product}.")
		return r3sponse.success_response(f"Successfully retrieved the id from product {product}.", {
		 	"id":plan_id,
		})
	def get_plan_id(self, product=None, plan=None):
		try: plan_id = self.plan_ids[product][plan]
		except KeyError: return r3sponse.error_response(f"Unable to find the id from plan {plan} product {product}.")
		return r3sponse.success_response(f"Successfully retrieved the id from plan {plan} product {product}.", {
		 	"id":plan_id,
		})
	def get_product_id_by_plan_id(self, plan_id):
		for _product_, _plans_ in self._subscriptions_.items():
			for _plan_name_, plan_info in _plans_.items():
				if self.plan_ids[_product_][_plan_name_] == plan_id:
					return r3sponse.success_response(f"Successfully retrieved the product id of plan id {plan_id}.", {
						"id":self.product_ids[_product_],
					})
		return r3sponse.success_response(f"Unable to find the the product id of plan id {plan_id}.")
	def get_product_name(self, id=None):
		for product, _id_ in self.product_ids.items():
			if _id_ == id:
				return r3sponse.success_response(f"Successfully retrieved the name of product {id}.", {
				 	"name":product,
				})
		return r3sponse.error_response(f"Unable to find the name of product {id}.")
	def get_plan_name(self, id=None):
		for product, ids in self.plan_ids.items():
			for plan, _id_ in ids.items():
				if _id_ == id:
					return r3sponse.success_response(f"Successfully retrieved the name of plan {id}.", {
					 	"name":plan,
					})
		return r3sponse.error_response(f"Unable to find the name of plan {id}.")

	# the defaults object.
	class Defaults(syst3m.objects.Object):
		def __init__(self,
			# the stripe secret key.
			secret_key=None,
			# 	the stripe publishable key.
			publishable_key=None,
			# the default products.
			products=None,
			# the domain.
			domain=None,
			# stripe object.
			stripe=None,
			# logging object.
			logging=None,
		):

			# custom defaults.
			syst3m.objects.Object.__init__(self)

			# arguments.
			self.secret_key = secret_key
			self.publishable_key = publishable_key
			self._subscriptions_ = products
			self.domain = domain
			self.stripe = stripe
			self.logging = logging

			#

	# the customers object.
	class Customers(syst3m.objects.Object):
		def __init__(self, defaults=None):
			
			# defaults.
			syst3m.objects.Object.__init__(self)
			self.assign(defaults.dict())

			# arguments.
			# ...
		def check(self, 
			# the users email.
			email=None,
		):

			# params.
			response = r3sponse.check_parameters({
				"email":email,})
			if not response.success: return response

			# check customer existance.
			response = self.get()
			if not response.success: return response
			exists, id = False, None
			for _id_, info in response.customers.items():
				if info["email"] == email:
					id = _id_
					exists = True
					break

			# handler.
			return r3sponse.success_response(f"Successfully checked the stripe customer existsance of user {email}.", {
				"exists":exists,
				"id":id,
			})
		def create(self, 
			# the users email.
			email=None,
		):

			# params.
			response = r3sponse.check_parameters({
				"email":email,})
			if not response.success: return response

			# check customer existance.
			response = self.check(email)
			if not response.success: return response
			if response["exists"]:
				return r3sponse.error_response(f"User {email} already has a stripe customer [{response['id']}].")

			# request.
			try:
				response = self.stripe.Customer.create(email=email)
			except Exception as e: return __handle_stripe_exception__(e)

			# handle.
			try:
				customer_id = response["id"]
				success = response["object"] == "customer" and "cus_" in customer_id
				if not success: raise KeyError("")
				return r3sponse.success_response(f"Successfully created a stripe customer for user {email}.", {
					"email":email,
					"id":customer_id,
				})
			except KeyError:
				return r3sponse.error_response(f"Failed to create stripe customer for user {email}, stripe response: {response}.")

			#
		def delete(self, 
			# the stripe customer id.
			id=None,
		):

			# params.
			response = r3sponse.check_parameters({
				"id":id,})
			if not response.success: return response

			# request.
			try:
				response = self.stripe.Customer.delete(id)
			except Exception as e: return __handle_stripe_exception__(e)

			# handle.
			try:
				success = response["deleted"] == True
				if not success: raise KeyError("")
				return r3sponse.success_response(f"Successfully deleted stripe customer {id}.", {
					"id":id,
				})
			except KeyError:
				return r3sponse.error_response(f"Failed to delete stripe customer {id}, stripe response: {response}.")

			#
		def get_id(self,
			# the users email.
			email=None,
		):
			response = self.get()
			if not response.success: return response
			for customer_id, info in response.customers.items():
				if info["email"] == email:
					return r3sponse.success_response(f"Successfully retrieved the stripe customer id of user {email}.", {
						"id":customer_id,
					})
			return r3sponse.error_response(f"Unable to find a stripe customer for user {email}.")		
		def get(self,
			# the stripe customer id (optional).
			id=None,
		):

			try:
				listed = self.stripe.Customer.list()
			except Exception as e: return __handle_stripe_exception__(e)

			# iterate.
			customers = {}
			for customer in listed['data']:
				customers[customer["id"]] = customer

			# by all.
			if id == None:
				
				# success.
				return r3sponse.success_response(f"Successfully retrieved {len(customers)} customer(s).", {
					"customers":customers,
				})

			# by id.
			else:
				try:
					return r3sponse.success_response(f"Successfully retrieved the customer [{id}].", {
						"customer":customers[id],
					})
				except KeyError:
					return r3sponse.error_response(f"Unable to find customer [{id}].")

			#
		def get_cards(self, 
			# the stripe customer id.
			id=None,
		):

			# params.
			response = r3sponse.check_parameters({
				"id":id,})
			if not response.success: return response

			# check customer existance.
			response = self.get(id=id)
			if not response.success: return response

			# request.
			try:
				response = self.stripe.Customer.list_sources(id, object="card",)
			except Exception as e: return __handle_stripe_exception__(e)
			
			# handle.
			try:
				data = response["data"]
			except KeyError:
				return r3sponse.error_response(f"Failed to retrieve the cards of user {id}, stripe response: {response}.")

			# serialize.
			cards = {}
			for item in data:
				item["card_cvc"] = f"***"
				item["card_name"] = str(item["name"])
				item["card_expiration_month"] = str(item["exp_month"])
				item["card_expiration_year"] = str(item["exp_year"])
				item["card_number"] = f"************{item['last4']}"
				del item["exp_year"]
				del item["exp_month"]
				del item["name"]
				cards[item["id"]] = item

			# success.
			return r3sponse.success_response(f"Successfully listed {len(cards)} card(s) of user {id}.", {
				"cards":cards,
			})

			#
		def create_card(self,
			# the stripe customer id.
			id=None,
			# the card holders name.
			name=None,
			# the card number.
			number=None,
			# the card expiration month.
			month=None,
			# the card expiration year.
			year=None,
			# the card cvc.
			cvc=None,
		):

			# params.
			response = r3sponse.check_parameters({
				"id":id,
				"number":number,
				"month":month,
				"year":year,
				"cvc":cvc,})
			if not response.success: return response
			number = number.replace(" ","").replace("-","").replace("_","").replace(" ","").replace(" ","").replace(" ","").replace(" ","")

			# get cards.
			response = self.get_cards(id=id)
			if not response.success: return response
			cards = response["cards"]

			# set source.
			try:
				token = self.stripe.Token.create(card={
					"name":name,
					"number": number,
					"exp_month": month,
					"exp_year": year,
					"cvc": cvc,
				})
			except Exception as e: return __handle_stripe_exception__(e)
				
			# handle.
			try:
				token_id = token["id"]
				success = token["object"] == "token" and "tok_" in token_id
				if not success: raise KeyError("")
			except KeyError:
				return r3sponse.error_response(f"Failed to create a card for user {id}, stripe response: {token}.")

			# create request.
			if len(cards) == 0:
				try:
					response = self.stripe.Customer.create_source(id, source=token)
				except Exception as e: return __handle_stripe_exception__(e)

			# update request.
			else:
				
				# delete.
				try:
					response = self.stripe.Customer.delete_source(id, list(cards.keys())[0],)
				except Exception as e: return __handle_stripe_exception__(e)
				try:
					success = response["deleted"] == True
					if not success: raise KeyError("")
				except KeyError:
					return r3sponse.error_response(f"Failed to delete card {card} from user {id}, stripe response: {response}.")

				# create.
				try:
					response = self.stripe.Customer.create_source(id, source=token)
				except Exception as e: return __handle_stripe_exception__(e)
			
			# handle.
			try:
				card_id = response["id"]
				success = response["object"] == "card" and "card_" in card_id
				if not success: raise KeyError("")
				return r3sponse.success_response(f"Successfully saved payment method ************{response['last4']}.", {
					"customer_id":id,
					"card_id":card_id,
					#"source_id":"@@"
				})
			except KeyError:
				return r3sponse.error_response(f"Failed to create a card for user {id}, stripe response: {response}.")

			#
		def delete_card(self, 
			# the stripe customer id.
			id=None, 
		):
			
			# params.
			response = r3sponse.check_parameters({
				"id":id,})
			if not response.success: return response

			# get card id.
			response = self.get_cards(id=id)
			if not response.success: return response
			if len(response.cards) == 0:
				return r3sponse.error_response("There are no payment methods stored.")
			card = list(response.cards,keys())[0]

			# delete request.
			try:
				response = self.stripe.Customer.delete_source(id, card)
			except Exception as e: return __handle_stripe_exception__(e)
			
			# handle.
			try:
				success = response["deleted"] == True
				if not success: raise KeyError("")
				return r3sponse.success_response(f"Successfully deleted card {id}.", {
					"card_id":card_id,
				})
			except KeyError:
				return r3sponse.error_response(f"Failed to delete card {card} from user {id}, stripe response: {response}.")

	# the subscriptions object.
	class Subscriptions(syst3m.objects.Object):
		def __init__(self, defaults=None, customers=None):
			# defaults.
			syst3m.objects.Object.__init__(self)
			self.assign(defaults.dict())

			# arguments.
			self.customers = customers

			#
		def create(self, 
			# the email of the user that will be charged.
			email=None,
			customer_id=None, # instead of email for effienciency.
			# the plan ids (list).
			plans=[],
		):

			# params.
			if email == None and customer_id == None: return r3sponse.error_response("Specify one of the following parameters: [email, customer_id].")
			if not isinstance(plans, list): return r3sponse.error_response("The plans <website.stripe.subscriptions.create:plans> parameter requires to be a list.")

			# get customer id.
			if customer_id == None:
				response = self.customers.get_id(email=email)
				if not response.success: return response
				customer_id = response.customer_id

			# request.
			items = []
			for plan in plans:
				items.append({"price":plan})
			try:
				response = self.stripe.Subscription.create(
					customer=customer_id,
					items=items
				)
			except Exception as e: return __handle_stripe_exception__(e)
			
			# handle.
			try:
				subscription_id = response["id"]
				success = response["object"] == "subscription" and response["status"] == "active"
				if not success: raise KeyError("")
				return r3sponse.success_response(f"Successfully created subscription {id}.", {
					"id":subscription_id,
				})
			except KeyError:
				return r3sponse.error_response(f"Failed to create subscription {id}, stripe response: {response}.")

			#
		def get(self, 
			# a specfic user email (optional).
			email=None,
			# active subscription plans only.
			active_only=True,
			# by customer id (custumer id as keys values in return).
			by_customer_id=False,
		):
			try:
				listed = self.stripe.Subscription.list()
			except Exception as e: return __handle_stripe_exception__(e)

			# iterate.
			subscriptions = {}
			for subscription in listed['data']:
				
				customer = subscription["customer"]
				_email_ = self.stripe.Customer.retrieve(customer)["email"]					
				identifier = _email_
				if by_customer_id: identifier = customer
				subscriptions[identifier] = {}
				#	-	subscription plan summary:
				status = subscription["status"]
				if not active_only or (active_only and status != "canceled"): 
					subscription_plans = subscription['items']['data']
					for subscription_plan in subscription_plans:
						plan_id = subscription_plan['plan']['id']
						active = subscription_plan['plan']['active']
						if active in [True, "true", "True", "TRUE"]: active = True
						else: active = False
						if not active_only or (active_only and active):
							l_plan_id = str(plan_id)
							count = 0
							for i in list(subscriptions[identifier].keys()):
								if plan_id in i: count += 1
							if count == 0:
								subscription_ids = [subscription_plan['subscription']]
							else:
								subscription_ids = subscriptions[identifier][plan_id]["subscription_ids"]+[subscription_plan['subscription']]
							subscriptions[identifier][plan_id] = {
								"email":_email_,
								"active":active,
								"customer_id" : customer,
								"subscription_id":subscription_plan['subscription'],
								"plan_id":plan_id,
								"plan_nickname":subscription_plan['plan']['nickname'],
								"items":count+1,
								"subscription_ids":subscription_ids
							}

			# by all.
			if email == None:
				
				# success.
				return r3sponse.success_response("Successfully retrieved the subscriptions.", {
					"subscriptions":subscriptions,
				})

			# by email.
			else:
				try:
					return r3sponse.success_response(f"Successfully retrieved the subscriptions of user [{email}].", {
						"subscriptions":subscriptions[email],
					})
				except KeyError:
					return r3sponse.error_response(f"No subscriptions found for user [{email}].")

			# error.
			#except Exception as e:
			#	return r3sponse.error_response(f"Failed to retrieve the subscriptions, error: {e}.")

			#
		def cancel(self, 
			# option 1:
			# 	the stripe subscription id.
			subscription_id=None, 
			# option 2:
			# 	select a user identification option.
			email=None,
			# 	the stripe plan id.
			plan=None,
		):
			
			# check options.
			if subscription_id == None and (email == None or plan == None):
				return r3sponse.error_response(f"Define option 1 parameter [subscription_id], option 2: parameters [email, plan].")	

			# get subscription id.
			if subscription_id == None:
				response = self.get(email=email)
				if response.error != None: return response
				for _subscription_id_, info in response.subscriptions.items():
					if info["plan_id"] == plan:
						subscription_id = _subscription_id_
						break
				if subscription_id == None:
					return r3sponse.error_response(f"Unable to find any subscriptions for user {email} plan {plan}.")	

			# delete.
			try:
				r = self.stripe.Subscription.delete(subscription_id)
				success = r["status"] == "canceled"
			except Exception as e: success = str(e)

			# handle success.
			if success == True:
				return r3sponse.success_response(f"Successfully canceled the subscription for user [{email}] from plan [{plan}].")
			else:
				if isinstance(success, str):
					return r3sponse.error_response(f"Failed to cancel the subscription for user [{email}] from plan [{plan}], error: {success}.")
				else:
					return r3sponse.error_response(f"Failed to cancel the subscription for user [{email}] from plan [{plan}]")

			#
	
	# the plans object.
	class Plans(syst3m.objects.Object):
		def __init__(self, defaults=None, subscriptions=None):
			
			# defaults.
			syst3m.objects.Object.__init__(self)
			self.assign(defaults.dict())

			# arguments.
			self.subscriptions = subscriptions
			
			#
		def get(self,
			# the plan id (plan_***) (optional).
			id=None,
			# get the subscriptions of the plan.
			get_subscriptions=False,
			# get active subscriptions only (required get_subscriptions=True).
			active_only=True,
		):
			
			# request.
			try:
				response = self.stripe.Price.list()
			except Exception as e: return __handle_stripe_exception__(e)
			
			# handle response.
			try:
				data = response["data"]
			except KeyError:
				return r3sponse.error_response(f"Failed to retrieve the plans, stripe response: {response}.")

			# get subscriptions.
			subscriptions = {}
			if get_subscriptions:
				response = self.subscriptions.get(active_only=active_only, by_customer_id=True)
				if not response.success: return response
				subscriptions = response["subscriptions"]
					

			# handle instance.
			plans = {}
			if isinstance(data, list):
				for item in data:
					if get_subscriptions:
						plan_subscriptions = {}
						for customer_id,subs_info in subscriptions.items():
							for plan_id,info in subs_info.items():
								if info["plan_id"] == item["id"]:
									info["email"] = subs_info["email"]
									info["customer_id"] = subs_info["customer_id"]
									plan_subscriptions[customer_id] = info
						item["subscriptions"] = plan_subscriptions
					item["price"] = item["unit_amount"]/100 # round(item["unit_amount"]/100,2)
					plans[item["id"]] = item
			else: 
				return r3sponse.error_response(f"Failed to retrieve the plans, unkown data instance, data: {data}.")

			# by no id.
			if id == None:
				return r3sponse.success_response(f"Successfully listed {len(plans)} plan(s).", {
					"plans":plans,
				})
			# by id.
			else:
				try:
					return r3sponse.success_response(f"Successfully listed the plan {id}.", {
						"plans":plans[id],
					})
				except KeyError:
					return r3sponse.error_response(f"Unable to find plan {id}.")
		def create(self,
			# the plan id.
			id=None,
			# the product id.
			product=None,
			# price per month.
			price=None,
			# the price currencry.
			currency="eur",
			# recurring options (do not edit unless you know what you are doing).
			recurring={"interval": "month"},
		):

			# params.
			response = r3sponse.check_parameters({
				"id":id,
				"product":product,
				"price":price,
				"currency":currency,})
			if not response.success: return response

			# request.
			try:
				response = self.stripe.Price.create(
					nickname=id,
					unit_amount=price*100,
					currency=currency,
					recurring=recurring,
					product=product,
				)
			except Exception as e: return __handle_stripe_exception__(e)
			
			# handle.
			try:
				plan_id = response["id"]
				success = response["active"] == True
				if not success: raise KeyError("")
				return r3sponse.success_response(f"Successfully created product {id}.", {
					"name":id,
					"id":plan_id,
					"price":price,
					"currency":currency,
					"product":product,
				})
			except KeyError:
				return r3sponse.error_response(f"Failed to create product {id}, stripe response: {response}.")

	# the products object.
	class Products(syst3m.objects.Object):
		def __init__(self, defaults=None, plans=None):
			
			# defaults.
			syst3m.objects.Object.__init__(self)
			self.assign(defaults.dict())

			# arguments.
			self.plans = plans

			#
		def get(self,
			# the product id (prod_***) (optional).
			id=None,
			# get the plans of each products.
			get_plans=False,
			# get the subscription of each plan (requires get_plans=True).
			get_subscriptions=False,
			# get active subscriptions only (required get_subscriptions=True).
			active_only=True,
		):
			
			# request.
			try:
				response = self.stripe.Product.list()
			except Exception as e: return __handle_stripe_exception__(e)

			# handle response.
			try:
				data = response["data"]
			except KeyError:
				return r3sponse.error_response(f"Failed to retrieve the products, stripe response: {response}.")

			# get plans.
			plans = {}
			if get_plans:
				response = self.plans.get(get_subscriptions=get_subscriptions, active_only=active_only)
				if not response.success: return response
				plans = response["plans"]

			# handle instance.
			products = {}
			if isinstance(data, list):
				for item in data:
					if get_plans:
						product_plans = {}
						for plan_id,info in plans.items():
							if info["product"] == item["id"]:
								product_plans[plan_id] = info
						item["plans"] = product_plans
					products[item["id"]] = item
			else: 
				return r3sponse.error_response(f"Failed to retrieve the products, unkown data instance, data: {data}.")

			# by no id.
			if id == None:
				return r3sponse.success_response(f"Successfully listed {len(products)} product(s).", {
						"products":products,
					})
			# by id.
			else:
				try:
					return r3sponse.success_response(f"Successfully listed the product {id}.", {
						"products":products[id],
					})
				except KeyError:
					return r3sponse.error_response(f"Unable to find product {id}.")
		def create(self,
			# the product id.
			id=None,
			# the product desciption.
			description=None,
		):
			
			# params.
			response = r3sponse.check_parameters({
				"id":id,})
			if not response.success: return response
			
			# request.
			try:
				response = self.stripe.Product.create(
					id=id,
					name=id,
					description=description,
					statement_descriptor=self.domain,
				)
			except Exception as e: return __handle_stripe_exception__(e)
			
			# handle.
			try:
				id = response["id"]
				success = response["active"] == True
				if not success: raise KeyError("")
				return r3sponse.success_response(f"Successfully created product {id}.", {
					"name":id,
					"id":id,
				})
			except KeyError:
				return r3sponse.error_response(f"Failed to create product {id}, stripe response: {response}.")
