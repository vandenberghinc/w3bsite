#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *
from w3bsite.classes import utils
from w3bsite.classes import defaults as _defaults_

# pip imports.
from django.contrib.auth import authenticate, login
import firebase_admin
from firebase_admin import credentials, auth, firestore, _auth_utils

class FirebaseCLI(object):
	def __init__(self):
		a=1
	"""
		if "--install" in sys.argv:
			if not self.installed():
				self.install():
	def install(self):
		os.system("curl -sL https://firebase.tools | bash")
	def installed(self):
		return Files.exists("/usr/local/bin/firebase") or Files.exists("/usr/bin/firebase")
	def login(self):
		output = util.__execute_script__("firebase login")
	def projects(self):
		output = util.__execute_script__("firebase")
	"""
	
# the firebase class.
class Firebase(_defaults_.Defaults):
	def __init__(self, 
		# the firebase key.
		key=None, 
		# the firebase js config.
		firebase_js={},
		# defaults.
		defaults=None,
	):

		# docs.
		DOCS = {
			"module":"website.firebase", 
			"initialized":True,
			"description":[], 
			"chapter": "Firebase", }
		
		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# check arguments.
		#response = dev0s.response.parameters.check({
		#	#"ip":ip,
		#})
		#if not response.success: raise ValueError(response.error)
		

		# initialize firestore.
		# (except for double etc)
		try:
			cred = credentials.Certificate(key) # must still be edited through env variables.
			firebase_admin.initialize_app(cred)
		except ValueError:a=1
		self.firestore = FireStore()
		self.users = Users(defaults=defaults, firestore=self.firestore)

		# firebase template data.
		def __handle__(dictionary={}):
			new_dictionary = {}
			for key, value in dictionary.items():
				if isinstance(value, str) or isinstance(value, int) or value == None:
					new_dictionary[key.upper()] = value
				elif isinstance(value, dict):
					new_dictionary[key.upper()] = __handle__(value)
				else:
					raise ValueError(f"Cannot serialize template data from firebase_js key [{key}], value: [{value}].")
			return new_dictionary
		self.template_data["FIREBASE"] = __handle__(firebase_js)
		#

# the firestore class.
class FireStore(object):
	def __init__(self):
		
		# docs.
		DOCS = {
			"module":"website.firebase.firestore", 
			"initialized":True,
			"description":[], 
			"chapter": "Firebase", }

		# initialize firestore.
		self.db = firestore.client()

		#
	# system functions.
	def list(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc = doc.get()
			success = True
		except: success = False
		if not success:
			return dev0s.response.error(f"Failed to load document [{reference}].")
		if not isinstance(doc, list):
			return dev0s.response.error(f"Reference [{reference}] leads to a document, not a collection.")
		return dev0s.response.success(f"Successfully listed the content of collection [{reference}].", {"collection":doc})
	def load(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc = doc.get()
			success = True
		except: success = False
		if not success:
			return dev0s.response.error(f"Failed to load document [{reference}].")
		if isinstance(doc, list):
			return dev0s.response.error(f"Reference [{reference}] leads to a collection, not a document.")
		if not doc.exists:
			return dev0s.response.error(f"Document [{reference}] does not exist.")
		else:
			data = doc.to_dict()
			return dev0s.response.success(f"Successfully loaded document [{reference}].", {"data":data})
	def load_collection(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc = doc.get()
			success = True
		except: success = False
		if not success:
			return dev0s.response.error(f"Failed to load document [{reference}].")
		if isinstance(doc, dict):
			return dev0s.response.error(f"Reference [{reference}] leads to a document, not a collection.")
		data = []
		for i in doc:
			if i.exists:
				data.append(i.id)
		return dev0s.response.success(f"Successfully loaded the document names of collection [{reference}].", {"collection":data, "documents":doc})
	def save(self, reference, data):
		doc = self.__get_doc__(reference)
		try:
			doc.set(data)
			success = True
		except: success = False
		if success:
			return dev0s.response.success(f"Successfully saved document [{reference}].")
		else:
			return dev0s.response.error(f"Failed to save document [{reference}].")
	def delete(self, reference):
		doc = self.__get_doc__(reference)
		try:
			doc.delete()
			success = True
		except: success = False
		if success:
			return dev0s.response.success(f"Successfully deleted document [{reference}].")
		else:
			return dev0s.response.error(f"Failed to delete document [{reference}].")
	# system functions.
	def __get_doc__(self, reference):
		reference = reference.replace("//", "/")
		if reference[len(reference)-1] == "/": reference = reference[:-1]
		doc, c = None, 0
		for r in reference.split("/"):
			if doc == None:
				doc = self.db.collection(r)
				c = 1
			else:
				if c == 1:
					doc = doc.document(r)
					c = 0
				else:
					doc = doc.collection(r)
					c = 1
		return doc

# the firebase users class.
# firebase users are no longer created, just in firestore database & django.
class Users(_defaults_.Defaults):
	def __init__(self, defaults=None, firestore=None):
		
		# docs.
		DOCS = {
			"module":"website.firebase.users", 
			"initialized":True,
			"description":[], 
			"chapter": "Firebase", }

		# defaults.
		_defaults_.Defaults.__init__(self)
		self.assign(defaults.dict())

		# objects.
		self.firestore = firestore

		#
	def get(self, 
		# define one of the following parameters.
		uid=None,
		email=None,
		phone_number=None,
	):
		try:
			user, variable = None, None
			if uid not in [None, "None", ""]:
				user = auth.get_user(uid)
				variable = str(uid)
			elif email not in [None, "None", ""]:
				user = auth.get_user_by_email(email)
				variable = str(email)
			elif phone_number not in [None, "None", ""]:
				user = auth.get_user_by_phone_number(phone_number)
				variable = str(phone_number)
			else:
				return dev0s.response.error("Invalid usage, define one of the following parameters: [uid, email, phone_number].")
		except _auth_utils.UserNotFoundError:
			return dev0s.response.error("User does not exist.")

		# check success.
		if user == None: 
			return dev0s.response.error(f"Failed to retrieve user [{variable}].")
		else:
			return dev0s.response.success(f"Successfully retrieved user [{variable}].", {"user":user})


		#
	def create(self,
		# required:
		email=None,
		password=None,
		verify_password=None,
		# optionals:
		name=None,
		phone_number=None,
		photo_url=None,
		email_verified=False,
	):

		# check parameters.
		response = dev0s.response.parameters.check(default=None, parameters={
			"email":email,
			"password":password,
			"verify_password":verify_password,
		})

		# check password.
		password = str(password)
		verify_password = str(verify_password)
		if len(password) < 8:
			return dev0s.response.error("The password must contain at least 8 characters.")
		elif password.lower() == password:
			return dev0s.response.error("The password must regular and capital letters.")
		elif password != verify_password:
			return dev0s.response.error("Passwords do not match.")

		# create.
		try:
			user = auth.create_user(
				email=email,
				email_verified=email_verified,
				phone_number=phone_number,
				password=password,
				display_name=name,
				photo_url=photo_url,
				disabled=False)
			success = True
		except Exception as e: 
			success = False
			error = e

		# handle error.
		if not success:
			return dev0s.response.error(f"Failed to create user [{email}], error: {error}")

		# handle success.
		return dev0s.response.success(f"Successfully created user [{email}].", {
			"user":user,
			"uid":user.uid,
			"email":user.email,
		})

		#
	def update(self,
		# required:
		email=None,
		# optionals:
		name=None,
		password=None,
		verify_password=None,
		phone_number=None,
		photo_url=None,
		email_verified=None,
	):

		# load.
		response = self.get(email=email)
		if response.error != None: return response
		user = response["user"]
		uid = user.uid

		# set defaults.
		if name == None: 
			#name = user.display_name # firebase
			name = user.display_name # firebase
		if email == None: email = user.email
		if phone_number == None: phone_number = user.phone_number
		if photo_url == None: photo_url = user.photo_url
		if email_verified == None: email_verified = user.email_verified
		if password != None and verify_password != None:
			# check password.
			password = str(password)
			verify_password = str(verify_password)
			if len(password) < 8:
				return dev0s.response.error("The password must contain at least 8 characters.")
			elif password.lower() == password:
				return dev0s.response.error("The password must regular and capital letters.")
			elif password != verify_password:
				return dev0s.response.error("Passwords do not match.")

		# create
		try:
			user = auth.update_user(
				uid,
				email=email,
				phone_number=phone_number,
				email_verified=email_verified,
				password=password,
				display_name=name,
				photo_url=photo_url,
				disabled=False)
			success = True
		except Exception as e: 
			success = False
			error = e

		# handle success.
		if success:
			return dev0s.response.success(f"Successfully updated user [{uid}].")
		else:
			return dev0s.response.error(f"Failed to update user [{uid}], error: {error}")

		#
	def delete(self, 
		# option 1:
		# the user's uid (much faster).
		uid=None,
		# option 2:
		# the users email / username.
		email=None,
	):
		if uid != None:
			try:
				auth.delete(uid)
				success = True
			except Exception as e: 
				success = False
				error = e
			if not success:
				return dev0s.response.error(f"Failed to delete user [{uid}], error: {error}")
			response = self.firestore.delete(f"{self.users_subpath}/{uid}")
			if not response.success: return response
			return dev0s.response.success(f"Successfully deleted user [{uid}].")
		else:
			response = self.get(email=email)
			if not response.success: return response
			return self.delete(uid=response.user.uid)
	def verify_id_token(self, id_token):
		"""
			Javascript:
				firebase.auth().currentUser.getIdToken(/* forceRefresh */ true).then(function(id_token) {
				  // Send token to your backend via HTTPS
				  // ...
				}).catch(function(error) {
				  // Handle error
				});
		"""
		try:
			decoded_token = auth.verify_id_token(id_token)
			uid = decoded_token['uid']
			if uid == None: success = False
			else: success = True
		except Exception as e: 
			success = False
			error = e
		if not success:
			return dev0s.response.error(f"You are not signed in, error: {error}")
		response = self.get(uid=uid)
		if not response.success: return response
		user = response.user
		return dev0s.response.success("You are signed in.", {"uid":uid, "email":user.email})	

		#
		


