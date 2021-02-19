
# imports.
from w3bsite.classes.config import *
import zlib, base64, binascii, glob
from Crypto.PublicKey import RSA as _RSA_
from Crypto.Cipher import PKCS1_OAEP

# the rsa object class.
class RSA(object):
	def __init__(self, 
		# the private key.
		private_key=None,
		# the public key.
		public_key=None,
	):
		self.public_key_pem = public_key
		self.private_key_pem = private_key
		self.public_key = None
		self.private_key = None
	# key management.
	def generate_keys(self):
			
		# generate.
		key_pair = _RSA_.generate(4096, e=65537)
		public_key = key_pair.publickey()
		public_key_pem = public_key.exportKey()
		private_key_pem = key_pair.exportKey()


		# save.
		self.private_key_pem = private_key_pem.decode()
		self.public_key_pem = public_key_pem.decode()
		
		# response.
		return r3sponse.success_response("Successfully generated a key pair.")

		#
	def load_private_key(self):

		# load keys.
		private_key = self.private_key_pem
		if private_key == None:
			return r3sponse.error_response("The private key is undefined.")

		# initialize keys.
		try:
			private_key = _RSA_.importKey(private_key)
		except Exception as e:
			return r3sponse.error_response(f"Exception: {e}")
		
		# response.
		self.private_key = private_key
		return r3sponse.success_response("Successfully loaded the private key.")

		#
	def load_public_key(self):

		# load keys.
		public_key = self.public_key_pem
		if public_key == None:
			return r3sponse.error_response("The public key is undefined.")

		# initialize keys.
		try:
			public_key = _RSA_.importKey(public_key)
		except Exception as e:
			return r3sponse.error_response(f"Exception: {e}")
		
		# response.
		self.public_key = public_key
		return r3sponse.success_response("Successfully loaded the public key.")

		#
	# encrypting & decrypting.
	def encrypt(self, string):

		# encrypt.
		encrypted = self.__encrypt_blob__(string, self.public_key)

		# response.
		return r3sponse.success_response(f"Successfully encrypted the string.", {
			"encrypted": encrypted,
		})

		#
	def decrypt(self, string):
		
		# decrypt.
		if isinstance(string,str): string = string.encode()
		decrypted = self.__decrypt_blob__(string, self.private_key)
		
		# response.
		return r3sponse.success_response(f"Successfully decrypted the string.", {
			"decrypted": decrypted,
		})

		#
	# system functions.
	def __encrypt_blob__(self, blob, public_key, silent=True):
		#Import the Public Key and use for encryption using PKCS1_OAEP
		rsa_key = public_key
		rsa_key = PKCS1_OAEP.new(rsa_key)

		#compress the data first
		try: 
			blob = zlib.compress(blob.encode())
		except: 
			blob = zlib.compress(blob)
		
		#In determining the chunk size, determine the private key length used in bytes
		#and subtract 42 bytes (when using PKCS1_OAEP). The data will be in encrypted
		#in chunks
		chunk_size = 470
		offset = 0
		end_loop = False
		encrypted = bytearray()
		max_offset, progress = len(blob), 0
		if silent == False: print(f'Encrypting {max_offset} bytes.')
		while not end_loop:
			#The chunk
			chunk = blob[offset:offset + chunk_size]

			#If the data chunk is less then the chunk size, then we need to add
			#padding with " ". This indicates the we reached the end of the file
			#so we end loop here
			if len(chunk) % chunk_size != 0:
				end_loop = True
				#chunk += b" " * (chunk_size - len(chunk))
				chunk += bytes(chunk_size - len(chunk))
			#Append the encrypted chunk to the overall encrypted file
			encrypted += rsa_key.encrypt(chunk)

			#Increase the offset by chunk size
			offset += chunk_size
			l_progress = round((offset/max_offset)*100,2)
			if l_progress != progress:
				progress = l_progress
				if silent == False: print('Progress: '+str(progress), end='\r')

		#Base 64 encode the encrypted file
		return base64.b64encode(encrypted)
	def __decrypt_blob__(self, encrypted_blob, private_key, silent=True):

		#Import the Private Key and use for decryption using PKCS1_OAEP
		rsakey = private_key
		rsakey = PKCS1_OAEP.new(rsakey)

		#Base 64 decode the data
		encrypted_blob = base64.b64decode(encrypted_blob)

		#In determining the chunk size, determine the private key length used in bytes.
		#The data will be in decrypted in chunks
		chunk_size = 512
		offset = 0
		decrypted = bytearray()
		max_offset = len(encrypted_blob)
		progress = 0
		if silent == False: print(f'Decrypting {max_offset} bytes.')
		#keep loop going as long as we have chunks to decrypt
		while offset < len(encrypted_blob):
			#The chunk
			chunk = encrypted_blob[offset: offset + chunk_size]

			#Append the decrypted chunk to the overall decrypted file
			decrypted += rsakey.decrypt(chunk)

			#Increase the offset by chunk size
			offset += chunk_size
			l_progress = round((offset/max_offset)*100,2)
			if l_progress != progress:
				progress = l_progress
				if silent == False: print('Progress: '+str(progress), end='\r')

		#return the decompressed decrypted data
		return zlib.decompress(decrypted)