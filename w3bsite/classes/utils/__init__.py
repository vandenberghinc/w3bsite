#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import * 
from w3bsite.classes.cache import cache
import xmltodict 


# the utils object class.
class Utils(Object):
	def __init__(self, attributes={}):

		# defaults.
		Object.__init__(self, traceback="Website.utils")
		self.assign(attributes)

		#

	# create template data.
	def template(self, old={}, new={}, safe=False):
		if isinstance(old, (Dictionary)):
			old = dict(old.dictionary)
		else:
			old = dict(old)
		if old == None or old == "None": old = {}
		if new == None or new == "None": return old
		if isinstance(new, (Dictionary)):
			new = new.dictionary
		elif isinstance(new, (OutputObject, ResponseObject)):
			new = new.dict()
		if not isinstance(new, (dict)):
			raise dev0s.exceptions.InvalidUsage(f"<website.utils.template>: Parameter [new] requires to be a [dict] not [{new.__class__.__name__}] ({new}).")
		if not isinstance(old, (dict, Dictionary)):
			raise dev0s.exceptions.InvalidUsage(f"<website.utils.template>: Parameter [old] requires to be a [dict, Dictionary] not [{new.__class__.__name__}] ({new}).")
		if new != old:
			new = Dictionary(old) + new
		#print("==================================================\nTEMPLATE DATA\n")
		#try: print(json.dumps(new, indent=4))
		#except: print(new)
		if isinstance(new, (Dictionary)): new = new.dictionary
		if safe:
			return self.serialize_template(new)
		else:
			return new

	# serialize dictionary to template safe dict.
	def serialize_template(self, value={}):
		if isinstance(value, (dict, Dictionary, OutputObject, ResponseObject)):
			if isinstance(value, (OutputObject, ResponseObject)):
				value = value.dict()
			new = {}
			for key, _value_ in value.items():
				new[key] = self.serialize_template(_value_)
			return new
		elif isinstance(value, (list, Array)):
			new = []
			for _value_ in value:
				new.append(self.serialize_template(_value_))
			return new
		elif isinstance(value, (float, Integer)):
			return float(value)
		elif isinstance(value, (int)):
			return int(value)
		else:
			return str(value)
		
	# catch request error.
	def catch_error(self, error):
		try:
			database = self.database
		except AttributeError:
			database = None
		if database == None:
			database = dev0s.env.get("DATABASE", default=None)
		if database != None and Files.exists(database):
			if not Files.exists(f"{database}/logs"): os.mkdir(f"{database}/logs")
			dev0s.response.log_file = gfp.clean(f"{database}/logs/errors")
		trace = traceback.format_exc()
		print(trace)
		id = String().generate(length=32, digits=True, capitalize=True)
		if database != None and Files.exists(database):
			dev0s.response.log_to_file("\n----------------------------------------------------------\n", raw=True)
			dev0s.response.log_to_file("Exception ("+str(id)+").\n ")
			dev0s.response.log_to_file(trace, raw=True)
			dev0s.response.log_to_file(" ", raw=True)
		info = {
			"id":id,
			"traceback":trace,
		}
		return info

		#

	# get naked domain url.
	def naked_url(self, domain):
		while True:
			if "https://" in domain:
				domain = domain.replace("https://","")
			elif "http://" in domain:
				domain = domain.replace("http://","")
			elif domain[len(domain)-1] == "/": domain = domain[:-1]
			elif domain[0] == "/": domain = domain[1:]
			else: break
		return domain

		#

	# get the client's ip address.
	def get_client_ip(self, request):
		try:
		    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		    if x_forwarded_for:
		        ip = x_forwarded_for.split(',')[0]
		    else:
		        ip = request.META.get('REMOTE_ADDR')
		    return ip
		except: return "unknown"

	#

# initialized globally.
utils = Utils()


# DEPRICATED

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
		if not Files.exists(path):

			# api request.
			url = f"https://api.vandenberghinc.com/packages/download/?package={package}&path={path}"
			try: response = requests.get(url)
			except Exception as e: return dev0s.response.error(f"Failed to install package file {package}:{path} from source {url}, error: {e}")	

			# handle response.
			try: response = response_object.json()
			except:
				return dev0s.response.error(f"Failed to install package file {package}:{path} from source {url}, error: {e}")
			if not response.success:
				return dev0s.response.error(f"Failed to install package file {package}:{path} from source {url}, error: {e}")

			# write out.
			try:
				open(path, 'wb').write(response_object.content)
			except:
				return dev0s.response.error(f"Failed to write out downloaded path [{path}].", log_level=0)	
			if not zip.file_path.exists():
				return dev0s.response.error(f"Failed to write out downloaded path [{path}].", log_level=0)

	# success.
	return dev0s.response.success(f"Successfully checked {len(tuple_list)} libary file(s).")
			
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
	except: return "unknown"
	

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
	fp = FilePath(path)
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
	return dev0s.response.ResponseObject({
		"success":False,
		"error":None,
		"message":None,
	})

