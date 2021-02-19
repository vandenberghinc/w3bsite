#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import * 
import xmltodict 


# get naked domain url.
def naked_url(domain):
	while True:
		if "https://" in domain:
			domain = domain.replace("https://","")
		elif "http://" in domain:
			domain = domain.replace("http://","")
		elif domain[len(domain)-1] == "/": domain = domain[:-1]
		elif domain[0] == "/": domain = domain[1:]
		else: break
	return domain

# equalize file paths.
def equalize_path(variable, striplast=False):
	while True:
		if striplast and len(variable) > 0 and variable[len(variable)-1] == "/": variable = variable[:-1]
		elif "//" in variable: variable = variable.replace("//","/")
		else: break
	return variable

# check install vandenberghinc package files.
def __check_package_files__(tuple_list):
	for path, package, source in tuple_list:
		if not os.path.exists(path):

			# api request.
			url = f"https://api.vandenberghinc.com/packages/download/?package={package}&path={path}"
			try: response = requests.get(url)
			except Exception as e: return r3sponse.error_response(f"Failed to install package file {package}:{path} from source {url}, error: {e}")	

			# handle response.
			try: response = response_object.json()
			except:
				return r3sponse.error_response(f"Failed to install package file {package}:{path} from source {url}, error: {e}")
			if not response.success:
				return r3sponse.error_response(f"Failed to install package file {package}:{path} from source {url}, error: {e}")

			# write out.
			try:
				open(path, 'wb').write(response_object.content)
			except:
				return r3sponse.error_response(f"Failed to write out downloaded path [{path}].", log_level=0)	
			if not zip.file_path.exists():
				return r3sponse.error_response(f"Failed to write out downloaded path [{path}].", log_level=0)

	# success.
	return r3sponse.success_response(f"Successfully checked {len(tuple_list)} libary file(s).")
			
# append an old dict with a new one, optoinally overwrite the new keys.
def __append_dict__(old={}, new={}, overwrite=False):
	combined = dict(old)
	for key in list(new.keys()):
		try: old[key] ; new_key = False
		except KeyError: new_key = True
		if new_key or (not new_key and overwrite):
			combined[key] = new[key]
		else:
			combined[key] = old[key]
	return combined

# iterate a string backwards to check the first occurency of a specified charset.
def __first_occurence_reversed__(string="", charset=[" ", "\n"]):
	c, space_newline_id = len(string)-1, ""
	for _ in string:
		char = string[c]
		if char in charset:
			a = 0
			for i in charset:
				if i == char: return i
		c -= 1
	return None

# splice a string into before/after by a first occurence.
# if include is True and both include_before and inluce_after are False it includes at before.
def __before_after_first_occurence__(string="hello my world", slicer=" ", include=True, include_before=False, include_after=False): 
	before, after, slice_count, slices, _last_ = "", "", string.count(slicer), 0, ""
	for char in string:
		if len(_last_) >= len(slicer): _last_ = _last_[1:]
		_last_ += char
		if _last_ == slicer: 
			slices += 1
			if include:
				if slices != slice_count or include_before:
					before += char
				elif include_after:
					after += char
				else:
					before += char
		elif slices > 0:
			after += char
		else: 
			before += char
	return before, after

# splice a string into before/selected/after by a first occurence.
def __before_selected_after_first_occurence__(string="hello my world", slicer=" "):
	before, selected, after, slice_count, slices, _last_ = "", "", string.count(slicer), 0, ""
	for char in string:
		if len(_last_) >= len(slicer): _last_ = _last_[1:]
		_last_ += char
		if _last_ == slicer: 
			slices += 1
			selected += char
		elif slices > 0:
			after += char
		else: 
			before += char
	return before, selected, after

# splice a string into before/after by a last occurence.
# if include is True and both include_before and inluce_after are False it includes at before.
def __before_after_last_occurence__(string="hello my world", slicer=" ", include=True, include_before=False, include_after=False): 
	before, after, slice_count, slices, _last_ = "", "", string.count(slicer), 0, ""
	for char in string:
		if len(_last_) >= len(slicer): _last_ = _last_[1:]
		_last_ += char
		if _last_ == slicer: 
			slices += 1
			if include:
				if slices != slice_count or include_before:
					before += char
				elif include_after:
					after += char
				else:
					before += char
		elif slices == slice_count:
			after += char
		else: 
			before += char
	return before, after

# splice a string into before/selected/after by a last occurence.
def __before_selected_after_last_occurence__(string="hello my world", slicer=" "):
	before, selected, after, slice_count, slices, _last_ = "", "", "", string.count(slicer), 0, ""
	for char in string:
		if len(_last_) >= len(slicer): _last_ = _last_[1:]
		_last_ += char
		if _last_ == slicer: 
			slices += 1
			selected += char
		elif slices == slice_count:
			after += char
		else: 
			before += char
	return before, selected, after

# generate.
def __generate__(length=10, alphabetical=True, capitalize=True, digits=True):
	letters = ""
	if digits: letters += string.digits
	if capitalize: letters += string.ascii_uppercase
	if alphabetical: letters += string.ascii_lowercase
	return ''.join(random.choice(letters) for i in range(length))

# get the client ip of a request.
def get_client_ip(request):
	try:
	    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	    if x_forwarded_for:
	        ip = x_forwarded_for.split(',')[0]
	    else:
	        ip = request.META.get('REMOTE_ADDR')
	    return ip
	except: return "unkown"
def __get_client_ip__(request): # depricated.
	return get_client_ip(request)
	

# clean url.
def __clean_url__(url, strip_first_slash=False, strip_last_slash=False):
	while True:
		if "//" in url:
			url = url.replace("//","/")
		else: break
	if strip_first_slash:
		while True:
			if len(url) > 0 and url[0] == "/": url = url[1:]
			else: break
	if strip_last_slash:
		while True:
			if len(url) > 0 and url[len(url)-1] == "/": url = url[:-1]
			else: break
	return url

# convert xml to json.
def __xml_to_json__(xml):
    data_dict = xmltodict.parse(xml) 
    return json.loads(json.dumps(data_dict))

# execute a shell command.
def __execute__(
	# the command in array.
	command=[],
	# wait till the command is pinished. 
	wait=False,
	# the commands timeout, [timeout] overwrites parameter [wait].
	timeout=None, 
	# the commands output return format: string / array.
	return_format="string", 
	# the subprocess.Popen.shell argument.
	shell=False,
	# pass a input string to the process.
	input=None,
	# silent disabled shows all original command logs (experimental).
	silent=True,
):
	def __convert__(byte_array, return_format=return_format, silent=False):
		if return_format == "string":
			lines = ""
			for line in byte_array:
				if isinstance(line, str):
					lines += line
					if not silent:
						print(line.replace("\n",""))
				else:
					lines += line.decode()
					if not silent:
						print(line.decode().replace("\n",""))
			return lines
		elif return_format == "array":
			lines = []
			for line in byte_array:
				if isinstance(line, str):
					lines.append(line.replace("\n","").replace("\\n","").replace("\n\r","").replace("\r",""))
					if not silent:
						print(line.replace("\n","").replace("\\n","").replace("\n\r","").replace("\r",""))
				else:
					lines.append(line.decode().replace("\n","").replace("\\n","").replace("\n\r","").replace("\r",""))
					if not silent:
						print(line.decode().replace("\n","").replace("\\n","").replace("\n\r","").replace("\r",""))
			return lines

	# create process.
	if silent:
		p = subprocess.Popen(
			command, 
			shell=shell,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			stdin=subprocess.PIPE,)
	else:
		p = subprocess.Popen(
			command, 
			shell=shell,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE,
			stdin=subprocess.PIPE,
			universal_newlines=True,)
		_lines_ = ""
		for line in iter(p.stdout.readline, ""):
			_lines_ += line
		print(_lines_)
	
	# send input.
	if input != None:
		if isinstance(input, list):
			for s in input:
				p.stdin.write(f'{s}\n'.encode())
		elif isinstance(input, str):
			p.stdin.write(f'{input}\n'.encode())
		else: raise ValueError("Invalid format for parameter [input] required format: [string, array].")
		p.stdin.flush()
	
	# timeout.
	if timeout != None:
		time.sleep(timeout)
		p.terminate()
	
	# await.
	elif wait:
		p.wait()

	# get output.
	output = __convert__(p.stdout.readlines(), return_format=return_format, silent=silent)
	if return_format == "string" and output == "":
		output = __convert__(p.stderr.readlines(), return_format=return_format, silent=silent)
	elif return_format == "array" and output == []:
		output = __convert__(p.stderr.readlines(), return_format=return_format, silent=silent)
	return output

# execute a shell script.
def __execute_script__(
	# the script in string.
	script="",
	# wait till the command is pinished. 
	wait=False,
	# the commands timeout, [timeout] overwrites parameter [wait].
	timeout=None, 
	# the commands output return format: string / array.
	return_format="string", 
	# the subprocess.Popen.shell argument.
	shell=False,
	# pass a input string to the process.
	input=None,
	# silent disabled shows all original command logs (experimental).
	silent=True,
):
	path = "/tmp/shell_script.sh"
	__save_bytes__(path, script.encode())
	fp = Formats.FilePath(path)
	fp.permission.set(permission=755)
	output = __execute__(
		command=[f"sh", f"{path}"],
		wait=wait,
		timeout=timeout, 
		return_format=return_format, 
		shell=shell,
		input=input,
		silent=silent,)
	fp.delete(forced=True)
	return output

# save & load jsons.
def __load_json__(path):
	data = None
	with open(path, "r") as json_file:
		data = json.load(json_file)
	return data
def __save_json__(path, data):
	with open(path, "w") as json_file:
		json.dump(data, json_file, indent=4, ensure_ascii=False)

# save & load files.
def __load_file__(path):
	file = open(path,mode='rb')
	data = file.read().decode()
	file.close()
	return data
def __save_file__(path, data):
	file = open(path, "w+") 
	file.write(data)
	file.close()

# save & load bytes.
def __load_bytes__(path):
	file = open(path,mode='rb')
	bytes = file.read()
	file.close()
	return bytes
def __save_bytes__(path, bytes):
	file = open(path, "wb") 
	file.write(bytes)
	file.close()

# init a default response.
def __default_response__():
	return {
		"success":False,
		"error":None,
		"message":None,
	}

# the color object.
class Color(object):
	def __init__(self):
		self.purple = "\033[95m"
		self.cyan = "\033[96m"
		self.darkcyan = "\033[35m"
		self.orange = '\033[33m'
		self.blue = "\033[94m"
		self.green = "\033[92m"
		self.yellow = "\033[93m"
		self.grey = "\033[90m"
		self.marked = "\033[100m"
		self.markedred = "\033[101m"
		self.markedgreen = "\033[102m"
		self.markedcyan= "\033[103m"
		self.unkown = "\033[2m"
		self.red = "\033[91m"
		self.bold = "\033[1m"
		self.underlined = "\033[4m"
		self.end = "\033[0m"
		self.italic = "\033[3m"
	def remove(self, string):
		if string == None: return string
		for x in [color.purple,color.cyan,color.darkcyan,color.orange,color.blue,color.green,color.yellow,color.grey,color.marked,color.markedred,color.markedgreen,color.markedcyan,color.unkown,color.red,color.bold,color.underlined,color.end,color.italic]: string = string.replace(x,'')
		return string
	def fill(self, string):
		if string == None: return string
		for x in [
			["&PURPLE&", color.purple],
			["&CYAN&", color.cyan],
			["&DARKCYAN&", color.darkcyan],
			["&ORANGE&", color.orange],
			["&BLUE&", color.blue],
			["&GREEN&", color.green],
			["&YELLOW&", color.yellow],
			["&GREY&", color.grey],
			["&RED&", color.red],
			["&BOLD&", color.bold],
			["&UNDERLINED&", color.underlined],
			["&END&", color.end],
			["&ITALIC&", color.italic],
		]: string = string.replace(x[0],x[1])
		return string
	def boolean(self, boolean, red=True):
		if boolean: return color.green+str(boolean)+color.end
		else: 
			if red: return color.red+str(boolean)+color.end
			else: return color.yellow+str(boolean)+color.end

# the symbol object.
class Symbol(object):
	def __init__(self):
		self.cornered_arrow = color.grey+'↳'+color.end
		self.cornered_arrow_white = '↳'
		self.good = color.bold+color.green+"✔"+color.end
		self.good_white = "✔"
		self.bad = color.bold+color.red+"✖"+color.end
		self.bad_white = "✖"
		self.medium = color.bold+color.orange+"✖"+color.end
		self.pointer = color.bold+color.purple+"➤"+color.end
		self.star = color.bold+color.yellow+"★"+color.end
		self.ice = color.bold+color.cyan+"❆"+color.end
		self.retry = color.bold+color.red+"↺"+color.end
		self.arrow_left = color.end+color.bold+"⇦"+color.end
		self.arrow_right = color.end+color.bold+"⇨"+color.end
		self.arrow_up = color.end+color.bold+"⇧"+color.end
		self.arrow_down = color.end+color.bold+"⇩"+color.end
		self.copyright = color.bold+color.grey+"©"+color.end
		self.heart = color.bold+color.red+"♥"+color.end
		self.music_note = color.bold+color.purple+"♫"+color.end
		self.celcius = color.bold+color.grey+"℃"+color.end
		self.sun = color.bold+color.yellow+"☀"+color.end
		self.cloud = color.bold+color.grey+"☁"+color.end
		self.moon = color.bold+color.blue+"☾"+color.end
		self.smiley_sad = color.bold+color.red+"☹"+color.end
		self.smiley_happy = color.bold+color.green+"☺"+color.end
		self.infinite = color.bold+color.blue+"∞"+color.end
		self.pi = color.bold+color.green+"π"+color.end
		self.mode = color.bold+color.purple+"ⓜ"+color.end
		self.action = color.bold+color.yellow+"ⓐ"+color.end
		self.info = color.bold+color.grey+"ⓘ"+color.end

	#

# default initialized classes.
color = Color()
symbol = Symbol()

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import formatdate

# the email object class.
class Email(object):
	def __init__(self, 
		email=None, # must be first parameter.
		password=None, # must be second parameter.
		smtp_host="smtp.gmail.com", 
		smtp_port=587, 
		use_tls=True,
		visible_email=None,
	):
		self.email = email
		self.visible_email = visible_email
		self.password = password
		self.smtp_host = smtp_host
		self.smtp_port = smtp_port
		self.use_tls = use_tls
		self.smtp = None
	def login(self, timeout=5):
		response = __default_response__()

		# try.
		try:
			smtp = smtplib.SMTP(self.smtp_host, self.smtp_port, timeout=timeout)
			if self.use_tls:
				smtp.starttls()
			smtp.login(self.email, self.password)
			self.smtp = smtp
		except AttributeError:
			response.error = "Define the email address & password."
			return response
		except smtplib.SMTPAuthenticationError:
			response.error = "Failed to log in, provided an incorrect email and password."
			return response
		except OSError as e:
			if "Network is unreachable" in str(e):
				response.error = "Failed to log in, the network is unreachable. Make sure you provided the correct smtp host & port."
				return response
			else:
				response.error = f"Failed to log in, error: {e}."
				return response

		# response.
		response["success"] = True
		response["message"] = f"Successfully logged in to the email [{self.email}]."
		return response
	def send(self,
		# the email's subject.
		subject="Subject.",
		# define either html or html_path.
		html=None,
		html_path=None,
		# the email's recipients.
		recipients=[],
		# optional attachments.
		attachments=[],
	):

		# checks.
		response = __default_response__()
		if html != None: a=1
		elif html_path == None: 
			response.error = "Define either parameter [html] or [html_path]."
			return response
		else: html = utils.__load_file__(html_path)
		if len(recipients) == 0: 
			response.error = "Define one or multiple recipients"
			return response

		# create message.
		try:

			msg = MIMEMultipart('alternative')
			if self.visible_email != None:
				msg['From'] = self.visible_email
			else:
				msg['From'] = self.email
			msg["To"] = ", ".join(recipients)
			msg['Date'] = formatdate(localtime=True)
			msg['Subject'] = subject
			
			# Create the body of the message (a plain-text and an HTML version).
			part1 = MIMEText("", 'plain')
			part2 = MIMEText("""\
				""" + html, 'html')
			msg.attach(part1)
			msg.attach(part2)
			for f in attachments or []:
				with open(f, "rb") as fil:
					part = MIMEApplication(
						fil.read(),
						Name=os.path.basename(f)
					)
				part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
				msg.attach(part)
			self.smtp.sendmail(self.email, recipients, msg.as_string())

			# response.
			response["success"] = True
			response["message"] = f"Succesfully send the email to {recipients}."
			return response
		except:
			response.error = f"Failed send the email to {recipients}."
			return response
