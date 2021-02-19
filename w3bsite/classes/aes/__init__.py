
# imports.
from w3bsite.classes.config import *
import base64, string, random
from Crypto.Cipher import AES as _AES_
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2


# the aes object class.
# AES 256 encryption/decryption using pycrypto library
class AES(object):
	def __init__(self, passphrase="MyPassphrase123!"):
		self.block_size = 16
		self.pad = lambda s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
		self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]
		self.passphrase = passphrase
	def encrypt(self, raw):
		if raw in ["", b"", None, False]:
			return r3sponse.error_response("Can not encrypt null data.")
		response = self.get_key()
		if not response.success: return response
		key = response["key"]
		salt = response["salt"]
		if isinstance(raw, bytes):
			raw = raw.decode()
		raw = self.pad(raw)
		iv = Random.new().read(_AES_.block_size)
		cipher = _AES_.new(key, _AES_.MODE_CBC, iv)
		encrypted = base64.b64encode(iv + salt + cipher.encrypt(raw.encode()))
		if raw != b"" and encrypted == b"":
			return r3sponse.error_response("Failed to encrypt the specified data with the current passphrase / salt.")
		return r3sponse.success_response("Successfully encrypted the specified data.", {
			"encrypted":encrypted,
		})
	def decrypt(self, enc):
		if enc in ["", b"", None, False]:
			return r3sponse.error_response("Can not decrypt null data.")
		if isinstance(enc, str):
			enc = enc.encode()
		enc = base64.b64decode(enc)
		iv_salt = enc[:32]
		iv = iv_salt[:16]
		salt = iv_salt[16:]
		response = self.get_key(salt=salt)
		if not response.success: return response
		key = response["key"]
		cipher = _AES_.new(key, _AES_.MODE_CBC, iv)
		decrypted = self.unpad(cipher.decrypt(enc[32:]))
		if enc != b"" and decrypted == b"":
			return r3sponse.error_response("Failed to decrypt the specified data with the current passphrase / salt.")
		return r3sponse.success_response("Successfully decrypted the specified data.", {
			"decrypted":decrypted,
		})
	def get_key(self, salt=None):
		if salt == None:
			salt = self.generate_salt()["salt"]
		if isinstance(salt, str):
			salt = salt.encode()
		kdf = PBKDF2(self.passphrase, salt, 64, 1000)
		key = kdf[:32]
		return r3sponse.success_response("Successfully loaded the aes key.", {
			"key":key,
			"salt":salt,
		})
	def generate_salt(self):
		length=16
		chars = ''.join([string.ascii_uppercase, string.ascii_lowercase, string.digits])
		salt = ''.join(random.choice(chars) for x in range(length))
		return r3sponse.success_response("Successfully generated a salt.", {
			"salt":salt,
		})