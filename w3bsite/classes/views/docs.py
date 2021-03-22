
# imports
from w3bsite.classes.views.defaults import *

# the documentations object class.
import importlib
class Documentations(View):
	def __init__(self):
		
		# docs.
		DOCS = {
			"module":"website.views.docs", 
			"initialized":True,
			"description":[], 
			"chapter": "Docs", }

		#
	def chapter(self,
		# the chapter title.
		title="Chapter Title",
		# the chapter's sections.
		sections=[],
		# whether the chapter is folded in the leftbar or not.
		folded=True,
	):
		return {
			"title":title,
			"sections":self.__assign_element_ids__(sections, key="element_id"),
			"sections_count":len(sections),
			"folded":folded,
			"element_id":self.__generate_element_id__(),
		}
	def section(self,
		# the title (str, list) (required).
		title="Section Title",
		# the description (str, list) (required).
		description=None,
		# the attributes (list) (required).
		attributes=[],
		# the parameters (list) (required).
		parameters=[],
		# the code areas (list) (required).
		code_areas=[],
		# system variables.
		# the section type (str) (required).
		type="section",
	):
		if isinstance(description, (list, Array)):
			description = Array(description).string(joiner="\n")
		description = self.__color_description__(description)
		return {
			"title":title,
			"description":description,
			"description_count":len(description),
			"attributes":self.__assign_element_ids__(attributes, key="element_id"),
			"attributes_count":len(attributes),
			"parameters":self.__assign_element_ids__(parameters, key="element_id"),
			"parameters_count":len(parameters),
			"code_areas":self.__assign_element_ids__(code_areas, key="element_id"),
			"code_areas_count":len(code_areas),
			"element_id":self.__generate_element_id__("sect_"),
			"type":type,
		}
	def subsection(self,
		# the title (str, list) (required).
		title="Sub Section Title",
		# the description (str, list) (required).
		description=None,
		# the attributes (list) (required).
		attributes=[],
		# the parameters (list) (required).
		parameters=[],
		# the code areas (list) (required).
		code_areas=[],
	):
		return self.section(
			title=title,
			description=description,
			attributes=attributes,
			parameters=parameters,
			code_areas=code_areas,
			type="subsection",
		)
	def parameter(self,
		# the parameters id.
		id="my_variable",
		# the parameters format (string / list with strings).
		format=None,
		# the parameters description.
		description=None,
		# whether the parameter is required or optional.
		required=False,
		# whether the parameter is folded by default or not.
		folded=False,
	):
		if isinstance(description, (list, Array)):
			description = Array(description).string(joiner="\n")
		return self.__parameter_attribute__(
			id=id,
			format=format,
			description=self.__color_description__(description),
			required=required,
			folded=folded,
			type="parameter",)
	def attribute(self,
		# the attributes id.
		id="my_variable",
		# the attributes format (string / list with strings).
		format=None,
		# the attributes description.
		description=None,
		# whether the attribute is folded by default or not.
		folded=False,
	):
		if isinstance(description, (list, Array)):
			description = Array(description).string(joiner="\n")
		return self.__parameter_attribute__(
			id=id,
			format=format,
			description=self.__color_description__(description),
			folded=folded,
			type="attribute",)
	def code_area(self,
		# the header title.
		title="my_variable",
		# the header subtitle.
		substitle=None,
		# the code area's content.
		content={
			"json":{},
			"python":"",
			# Unknown types are just non colored strings.
		},
		# the content css style with python_like or jsLike keys.
		styles={
			"height":"auto",
		},
	):
		# colors.
		def process_data(_data_):

			# normalize.
			_data_ = _data_.replace("	", "    ")
			data = _data_
			for key, replacer in [
				["\ndef  ", "\ndef "],
				["\nclass  ", "\nclass "],
			]:
				while True:
					if key in data: data = data.replace(key, replacer)
					else: break

			# chunk into array with
			parentheses = 0
			items = [] # [ [ $type, $lines ] ]
			chars, previous, lastchar, string_recognizer, string_open, string_closed = "", "default", None, None, False, False
			linecount = 0
			for char in data:
				if char == "\n":
					linecount += 1
				add_char = True
				refresh_parentheses = False
				if char == "(":
					if parentheses > 0:
						refresh_parentheses = True
					parentheses += 1
				elif char == ")":
					parentheses -= 1
					if parentheses > 0:
						refresh_parentheses = True
				if previous not in ["comment", "string"] and refresh_parentheses:
					items.append([previous, chars+char])
					chars = ""
					previous = "parentheses"
					add_char = False
				elif char == "#" and previous not in ["comment"]:
					items.append([previous, chars])
					chars = ""
					previous = "comment"
				elif previous == "comment" and char == "\n":
					items.append([previous, chars+char])
					add_char = False
					chars = ""
					previous = "default"
				elif previous not in ["comment"] and char in ["'", '"', "`"]:
					if previous in ["parentheses", "default"]:
						items.append([previous, chars])
						chars = ""
						previous = "string"
						string_recognizer = char
					elif previous == "string":
						if string_recognizer == char and lastchar != char:
							string_recognizer = None
							add_char = False
							items.append(["string", chars+char])
							chars = ""
							previous = "default"
					elif previous != None: raise ValueError(f"Unknown previous: {previous}")
				elif previous not in ["comment", "string"] and parentheses > 0:
					#if previous in ["string", "default", "comment"]:
					if previous != "parentheses":
						add_char = False
						items.append([previous, chars+char])
						chars = ""
						previous = "parentheses"
				elif previous == "parentheses" and parentheses <= 0:
					items.append([previous, chars])
					chars = ""
					previous = "default"
				elif previous not in ["string", "comment"]:
					if previous in ["string", "comment", "parentheses"]:
						items.append([previous, chars])
						chars = ""
					elif previous not in ["default",None]: raise ValueError(f"Unknown previous: {previous}")
					previous = "default"
				lastchar = char
				if add_char: chars += char

			# set remainder.
			items.append([previous, chars])
			return items

			#

		# color code.
		default = None
		words = {}
		for language, data in content.items():
			default = language
			if language == "json":

				# language functions.
				def process_items(items):

					# iterate items.
					words, count, max, next, next_chars, previous, previous_chars = [], 0, len(items)-1, None, None, None, None
					for type, chars in items:
						#print(type.upper(), chars)

						# get previous.
						if count == 0: previous = None
						else: previous,previous_chars = items[count-1]
						
						# get next.
						if count == max: next = None
						else: next,next_chars = items[count+1]

						# string.
						if type == "string":
							words.append(self.__create_word__(word=chars, color="yellow", type="string", joiner="", language=language))

						# comment.
						elif type == "comment":
							words.append(self.__create_word__(word=chars, color="grey", type="comment", joiner="", language=language))

						# else
						elif type == "default":
							words += process_default(chars, next=next, next_chars=next_chars)

						# increment count.
						count += 1

					# return.
					return words
				def process_default(chars, next=None, next_chars=None,):
					words = []
					last, keep = {}, 100
					for i in range(keep+1):
						if i > 0: last[str(i)] = ""
					_chars_, int_chars = "", ""
					integer_block = False
					for char in chars:
						add_char = True

						# integer chars.
						try: float(int_chars+char) ; integer = True
						except: integer = False
						if integer:
							integer_block = True
							int_chars += char
						elif int_chars != "":
							integer_block = False
							words.append(self.__create_word__(word=_chars_[:-len(int_chars)], joiner="", language=language))
							words.append(self.__create_word__(word=int_chars, color="purple", joiner="", language=language))
							int_chars = ""
							_chars_ = ""

						# add char.
						if add_char:
							_chars_ += char

						# last.
						for i in range(keep+1):
							if i > 0:
								if len(last[str(i)]) >= i:
									last[str(i)] = last[str(i)][1:]
								last[str(i)] += char

						# no integer.
						if not integer_block:

							# purple.
							for i in [
								" false ", " true ", " null ",
								" false,", " true,", " null,",
								":false ", ":true ", ":null ",
								":false,", ":true,", ":null,",
								":false\n", ":true\n", ":null\n",
								" false\n", " true\n", " null\n",
							]:
								if last[str(len(i))] == i:
									words.append(self.__create_word__(word=_chars_[:-len(i)], joiner="", language=language))
									words.append(self.__create_word__(word=i, color="purple", joiner="", language=language))
									_chars_ = ""
				
					# default remainder.
					words.append(self.__create_word__(word=_chars_, joiner="", language=language))
					return words

					#


				# process.
				if isinstance(data, dict):
					data = json.dumps(data, indent=4)
				elif not isinstance(data, str): raise ValueError(f"Unknown json code area content format: {data}")
				items = process_data(data)
				words[language] = process_items(items)

				#
			elif language == "python":

				# language functions.
				def process_items(items):

					# iterate items.
					words, count, max, next, next_chars, previous, previous_chars = [], 0, len(items)-1, None, None, None, None
					for type, chars in items:
						#print(type.upper(), chars)

						# get previous.
						if count == 0: previous = None
						else: previous,previous_chars = items[count-1]
						
						# get next.
						if count == max: next = None
						else: next,next_chars = items[count+1]

						# string.
						if type == "string":
							words.append(self.__create_word__(word=chars, color="yellow", type="string", joiner="", language=language))

						# comment.
						elif type == "comment":
							words.append(self.__create_word__(word=chars, color="grey", type="comment", joiner="", language=language))

						# parentheses.
						elif type == "parentheses":
							words += process_parentheses(chars, previous=previous, previous_chars=previous_chars)

						# default.
						elif type == "default":
							words += process_default(chars, next=next, next_chars=next_chars)

						# increment count.
						count += 1

					# return.
					return words
				def process_parentheses(chars, previous=None, previous_chars=None):
					
					# words.
					words = []
					
					# by class initialization.
					if previous_chars != None  and "class " in previous_chars:
						c, _chars_, last, spaces, success = len(previous_chars)-1, "", "", 0, False
						for _ in previous_chars:
							char = previous_chars[c]
							if char == " ": 
								if spaces > 0:
									success = False
									break 
								spaces += 1
							elif last == " ssalc":
								success = True
								break
							_chars_ += char
							if len(last) >= 6:
								last = last[1:]
							last += char
							c -=1
						if last == " ssalc" or success:
							for item in chars.split(","):
								words.append(self.__create_word__(word=item, color="green", italic=True, joiner=",", language=language))
							return words
					
					# by no class initialization.
					items = []
					_chars_, comma = "", True
					for char in chars:
						add_char = True
						if char == ",":
							comma = True
							if _chars_ != "":
								items.append(_chars_)
							_chars_ = ""
						elif comma:
							comma = False
							items.append(_chars_)
							_chars_ = ""
						if add_char: _chars_ += char
					items.append(_chars_)
					#
					for item in items:
						if item not in [""]:
							if item in [",", "\n"]:
								words.append(self.__create_word__(word=item, color=None, joiner="", language=language))
							elif "=" not in item:
								if "(" in item:
									slicer_id = str(String(item).first_occurence(charset=[" ", "\n", "\r"], reversed=True))
									if slicer_id == None: slicer_id = " "
									before, after = String(item).before_after_last_occurence(slicer=slicer_id, include_before=True)
									if len(after) > 0:
										words.append(self.__create_word__(word=before, joiner="", language=language))
									else:
										after = before
									if "." not in after:
										words.append(self.__create_word__(word=after[:-1], color="blue", joiner="", language=language))
										words.append(self.__create_word__(word="(", joiner="", language=language))
									else:
										before, after = String(after).before_after_last_occurence(slicer=".", include_before=True)
										words.append(self.__create_word__(word=before, joiner="", language=language))
										words.append(self.__create_word__(word=after[:-1], color="blue", joiner="", language=language))
										words.append(self.__create_word__(word="(", joiner="", language=language))
								elif item == "...":
									words.append(self.__create_word__(word=item, color="orange", italic=True, joiner="", language=language))
								else:
									words.append(self.__create_word__(word=item, color="orange", italic=True, joiner="", language=language))
							else:
								before, after = String(item).before_after_first_occurence(slicer="=", include=False)
								words.append(self.__create_word__(word=before, color="orange", italic=True, joiner="", language=language))
								words.append(self.__create_word__(word="=", color="red", joiner="", language=language))
								if "(" in after:
									if "." not in after:
										words.append(self.__create_word__(word=after[:-1], color="blue", joiner="", language=language))
										words.append(self.__create_word__(word="(", joiner="", language=language))
									else:
										before, after = String(after).before_after_last_occurence(slicer=".", include_before=True)
										words.append(self.__create_word__(word=before, joiner="", language=language))
										words.append(self.__create_word__(word=after[:-1], color="blue", joiner="", language=language))
										words.append(self.__create_word__(word="(", joiner="", language=language))
								else:
									afters, _chars_ = [], ""
									c, max = 0, len(after)-1
									for char in after:
										add_char = True
										try: float(_chars_) ; integer = True
										except: integer = False
										if integer:
											try: float(_chars_+char) ; new_integer = True
											except: new_integer = False
											if new_integer:
												a=1
											else:
												afters.append(self.__create_word__(word=_chars_, color="purple", joiner="", language=language))
												_chars_ = ""
										elif _chars_ in ["None", "True", "False"]:
											afters.append(self.__create_word__(word=_chars_, color="purple", joiner="", language=language))
											_chars_ = ""
										if add_char: _chars_ += char
									if _chars_ != "":
										try: float(_chars_) ; integer = True
										except: integer = False
										if integer:
											afters.append(self.__create_word__(word=_chars_, color="purple", joiner="", language=language))
										elif _chars_ in ["None", "True", "False"]:
											afters.append(self.__create_word__(word=_chars_, color="purple", joiner="", language=language))
										else:
											afters.append(self.__create_word__(word=_chars_, color=None, joiner="", language=language))
									c = 0
									for after in afters:
										if c == len(afters)-1:
											after["joiner"] = ""
											words.append(after)
										else:
											words.append(after)
										c += 1
					return words
				def process_default(chars, next=None, next_chars=None,):
					words = []
					parentheses_end = chars[len(chars)-1] == "("
					last, keep = {}, 100
					for i in range(keep+1):
						if i > 0: last[str(i)] = ""
					_chars_, slices, slicer_count, catch_function = "", 0, 0, False
					integer_block, int_chars, slicer_id = False, "", None
					if parentheses_end:
						slicer_id = str(String(chars).first_occurence(charset=[" ", "\n", "\r"], reversed=True))
						slicer_count = chars.count(slicer_id)
					firstline, lastchar, nextchar, charcount = True, None, None, 0
					for char in chars:
						if char in ["\n"]: firstline = False
						try: nextchar = chars[charcount+1]
						except: nextchar = None
						add_char = True

						# classes & functions.
						if char == slicer_id:
							slices += 1
						if parentheses_end and slicer_count > 0 and slices == slicer_count:
							if not catch_function:
								if last["5"] == "class":
									words.append(self.__create_word__(word=_chars_[:-len("class")], joiner="", language=language))
									words.append(self.__create_word__(word="class", color="blue", joiner="", language=language))
								elif last["3"] == "def":
									words.append(self.__create_word__(word=_chars_[:-len("def")], joiner="", language=language))
									words.append(self.__create_word__(word="def", color="blue", joiner="", language=language))
								elif last[str(len("__init__"))] == "__init__":
									words.append(self.__create_word__(word=_chars_[:-len("__init__")], joiner="", language=language))
									words.append(self.__create_word__(word="__init__", color="blue", joiner="", language=language))
								else:
									words.append(self.__create_word__(word=_chars_, joiner=""))
								_chars_ = ""
							elif char == "(":
								if last["5"] == "class":
									words.append(self.__create_word__(word=_chars_, color="green", joiner="", language=language))
								elif last["3"] == "def":
									words.append(self.__create_word__(word=_chars_, color="green", joiner="", language=language))
								else:
									if "." in _chars_:
										before, after_1 = String(_chars_).before_after_last_occurence(slicer=".", include_before=True)
										first = str(String(before).first_occurence(charset=[" string.", "\nstring."], reversed=True))
										if first != None:
											before, selected, after_2 = String(before).before_selected_after_first_occurence(slicer="first")
											words.append(self.__create_word__(word=before, joiner="", language=language))
											words.append(self.__create_word__(word=selected, color="orange", italic=True, joiner="", language=language))
											words.append(self.__create_word__(word=after_2, color="blue", joiner="", language=language))
										else:
											words.append(self.__create_word__(word=before, joiner="", language=language))
										words.append(self.__create_word__(word=after_1, color="blue", joiner="", language=language))
									else:
										words.append(self.__create_word__(word=_chars_, color="blue", joiner="", language=language))
								_chars_ = ""
							catch_function = True
							_chars_ += char

						# else.
						else:

							# integer chars.
							try: 
								float(int_chars+char)
								integer = True
							except: integer = False
							if integer:
								integer_block = True
								int_chars += char
							elif int_chars != "":
								integer_block = False
								"""
								nointeger = False
								for a in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
									for b in "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM":
										l_lastchar , l_nextchar = lastchar, nextchar
										if l_lastchar == None: l_lastchar = ""
										if l_nextchar == None: l_nextchar = ""
										if len(f"{l_nextchar}{int_chars}{l_nextchar}") < len(f"{a}{int_chars}{b}"): 
											nointeger = None
											break 
										if f"{a}{int_chars}{b}" == f"{l_nextchar}{int_chars}{l_nextchar}":
											nointeger = True
											break
									if nointeger in [True, None]: break
								"""
								#print(i)
								no_integer = False
								for i in [
									f" {int_chars}",
									f"\n{int_chars}",
									f"\r{int_chars}",
									f"({int_chars}",
									f"={int_chars}",
									f"+{int_chars}",
									f"-{int_chars}",
									"{"+f"{int_chars}",
								]:

									if last[str(len(i)+1)] in i:
										no_integer = True
								if no_integer:
									int_chars = ""
								else:
									words.append(self.__create_word__(word=_chars_[:-len(int_chars)], joiner="", language=language))
									words.append(self.__create_word__(word=int_chars, color="purple", joiner="", language=language))
									int_chars = ""
									_chars_ = ""
							"""
							try: float(_chars_) ; integer = True
							except: integer = False
							if integer:
								try: float(_chars_+char) ; new_integer = True
								except: new_integer = False
								if char == "." or new_integer:
									integer_block = True
								else:
									words.append(self.__create_word__(word=_chars_, color="purple", joiner="", language=language))
									_chars_ = ""
									integer_block = False
							else: integer_block = False
							"""

							# add char.
							if add_char:
								_chars_ += char

							# last.
							for i in range(keep+1):
								if i > 0:
									if len(last[str(i)]) >= i:
										last[str(i)] = last[str(i)][1:]
									last[str(i)] += char

							# no integer.
							if not integer_block:

								# red.
								local = []
								for i in ["if", "for", "elif", "else", "elif", "raise", "break", "try", "except", "return", "import", "del", "print"]:
									if firstline or last[str(len(i)+1)] == last[str(len(i))]:
										local.append(f"{i} ")
										local.append(f"{i}\n")
										local.append(f"{i}\r")
									local.append(f" {i} ")
									local.append(f" {i}\n")
									local.append(f" {i}\r")
									local.append(f"\n{i} ")
									local.append(f"\n{i}\n")
									local.append(f"\n{i}\r")
									local.append(f"\r{i} ")
									local.append(f"\r{i}\n")
									local.append(f"\r{i}\r")
								for i in [
									"+", "|", "&", "-", "=", ">", "<", "!", "@", 
									" in ", " or ",
									" try:","\ntry:"," except:","\nexcept:"," else:","\nelse:",
								]+local:
									#print(f"[{last[str(len(i))]}] VS [{i}], lastchar: [{lastchar}]")
									if last[str(len(i))] == i:
										words.append(self.__create_word__(word=_chars_[:-len(i)], joiner="", language=language))
										words.append(self.__create_word__(word=i, color="red", joiner="", language=language))
										_chars_ = ""

								# orange italic.
								local = []
								for i in ["self.", "self[", ]:
									if firstline or last[str(len(i)+1)] == last[str(len(i))]:
										local.append(f"{i}")
									local.append(f" {i}")
									local.append(f"\n{i}")
									local.append(f"\r{i}")
								for i in [
								]+local:
									if last[str(len(i))] == i:
										words.append(self.__create_word__(word=_chars_[:-len(i)], joiner="", language=language))
										words.append(self.__create_word__(word=i, color="orange", italic=True, joiner="", language=language))
										_chars_ = ""
								
								# purple.
								for i in [
									" False ", " True ", " None ",
									" False\n", " True\n", " None\n",
									" False\r", " True\r", " None\r",
									"...",
								]:
									#if i == "...":
									#	print(f"{i} VS [{last[str(len(i))]}]")
									if last[str(len(i))] == i:
										words.append(self.__create_word__(word=_chars_[:-len(i)], joiner="", language=language))
										words.append(self.__create_word__(word=i, color="purple", joiner="", language=language))
										_chars_ = ""
								
								# blue.
								for i in [
								]:
									if last[str(len(i))] == i:
										words.append(self.__create_word__(word=_chars_[:-len(i)], joiner="", language=language))
										words.append(self.__create_word__(word=i, color="blue", joiner="", language=language))
										_chars_ = ""

						# last char.
						lastchar = char
						charcount += 1

				
					# default remainder.
					words.append(self.__create_word__(word=_chars_, joiner="", language=language))
					return words

					#

				# process.
				if not isinstance(data, str):
					#lines = str(content[language]).split("\n")
					raise ValueError(f"Content of language {language} is not str format, {data}.")
				items = process_data(data)
				words[language] = [self.__create_word__(word="\n")] + process_items(items)

				#
			elif language in ["bash", "shell", "cli", "pip", "pip3", "curl"]:

				# language functions.
				def process_items(items):

					# iterate items.
					words, count, max, next, next_chars, previous, previous_chars = [], 0, len(items)-1, None, None, None, None
					for type, chars in items:
						#print(type.upper(), chars)

						# get previous.
						if count == 0: previous = None
						else: previous,previous_chars = items[count-1]
						
						# get next.
						if count == max: next = None
						else: next,next_chars = items[count+1]

						# string.
						if type == "string":
							words.append(self.__create_word__(word=chars, color="yellow", type="string", joiner="", language=language))

						# comment.
						elif type == "comment":
							words.append(self.__create_word__(word=chars, color="grey", type="comment", joiner="", language=language))

						# else
						elif type == "default":
							words += process_default(chars, next=next, next_chars=next_chars)

						# increment count.
						count += 1

					# return.
					return words
				def process_default(chars, next=None, next_chars=None,):
					words = []
					delimiters = [" ","\n"]
					scentence = ""
					word = ""
					for char in chars:

						# check delimiter.
						if char in delimiters:
							if (len(word) > 0 and word[0] == "-") or (len(word) > 1 and word[:2] == " -"):
								words.append(self.__create_word__(word=word, color="orange", italic=True, joiner="", language=language))
							elif len(word) > 0 and scentence == "":
								words.append(self.__create_word__(word=word, color="blue", joiner="", language=language))
							else:
								words.append(self.__create_word__(word=word, joiner="", language=language))
							scentence += word
							word = ""
							if char in "\n": scentence = ""


						# add word.
						word += char

				
					# default remainder.
					if word != "":
						if (len(word) > 0 and word[0] == "-") or (len(word) > 1 and word[:2] == " -"):
							words.append(self.__create_word__(word=word, color="orange", italic=True, joiner="", language=language))
						elif len(word) > 0 and scentence == "":
							words.append(self.__create_word__(word=word, color="blue", joiner="", language=language))
						else:
							words.append(self.__create_word__(word=word, joiner="", language=language))
					return words

					#


				# process.
				if isinstance(data, dict):
					data = json.dumps(data, indent=4)
				elif not isinstance(data, str): raise ValueError(f"Unknown json code area content format: {data}")
				items = process_data(data)
				words[language] = process_items(items)

			else:

				# no color.
				words[language] = [self.__create_word__(word=data, language=language)]

		# return.
		return {
			"title":title.upper(),
			"substitle":substitle,
			"words":words,
			"styles":styles,
			"default":default,
			"element_id":self.__generate_element_id__(),
		}
		#

	# system functions.
	def __parameter_attribute__(self,
		id="my_variable",
		format=None,
		description=None,
		required=False,
		folded=None,
		type=None,
	):
		if isinstance(format, str):
			format = [format]
		elif not isinstance(format, list):
			raise ValueError(f"Unknown format instance [{format}]. The format should be a list with formats or a single string format.")
		return {
			"id":id,
			"format":format,
			"description":description,
			"description_count":len(description),
			"folded":folded,
			"required":required,
			"element_id":self.__generate_element_id__(),
			"type":type,
		}
	def __generate_element_id__(self, joiner=""):
		return joiner+String("").generate(length=32, digits=True, capitalize=True)
		#
	def __create_word__(self, color=None, italic=False, type=None, word="", linecount=None, joiner="", language=None, styles={}):
		colors = {
			"red":"#FF0071",
			"green":"#93E600",
			"blue":"#25DBF2",
			"orange":"#FF9100",
			"yellow":"#E9DC61",
			"purple":"#B57AFF",
			"grey":"#75705B",
		}
		try: color = colors[color]
		except: color = None
		return {
			"value":word,
			"color":color,
			"italic":italic,
			"linecount":linecount,
			"language":language,
			"joiner":joiner,
			"type":type,
			"styles":styles,
		}
	def __color_description__(self, description):
		def clean_tag(tag):
			while True:
				if " " in tag: tag = tag.replace(" ", "")
				else: break
			return tag
		if isinstance(description, (list, Array)):
			description = Array(description).string(joiner="\n")
		words, c, open, closing, chars, max = [], 0, False, False, "", len(description)
		while c < max:
			add_char = True
			char = description[c]
			try: next = description[c+1]
			except: next = None
			if open and (char == "<" or (closing and char == ">")):
				if char == "<":
					closing = True
				elif closing and char == ">":
					add_char = False
					chars += char
					words.append(self.__create_word__(word=chars))
					chars = ""
					closing = False
					open = False
			elif not open and char == "<":
				open = True
				words.append(self.__create_word__(word=chars))
				chars = ""
			if add_char: chars += char
			c += 1
		if chars != "":
			words.append(self.__create_word__(word=chars))
		_words_ = []
		for word in words:
			if len(word["value"]) > 0 and word["value"][0] == "<":
				# style tags.
				tag = clean_tag(word["value"].split(">")[0]+">")
				word["value"] = word["value"][len(tag):]
				word["value"], _ = String(word["value"]).before_after_last_occurence(slicer="<", include=False)
				styles = {}
				# append styles.
				block = False
				if not block and tag in ["<bold>"]:
					block = True
					styles = Dictionary(styles) + {
						"font_weight":"700",}
				if not block and tag in ["<italic>"]:
					block = True
					styles = Dictionary(styles) + {
						"font_style":"italic",}
				if not block and tag in ["<code>", "<parameter>", "<attribute>"]:
					styles = Dictionary(styles) + {
						"background": f"#00000025", 
						"border":"1px solid #00000035",
						"border_radius":"10px",
						"font_family":"Courier New",
						"padding":"1.5px 7.5px 1.5px 7.5px",}
				if not block and tag in ["<parameter>", "<attribute>"]:
					styles = Dictionary(styles) + {
						"font_style":"italic",}
				# append tagless word.
				if isinstance(styles, (Dictionary)):
					styles = styles.dictionary
				if styles == {}:
					_words_.append(word)
				# append tag word.
				else:
					_words_.append(self.__create_word__(word=word["value"], styles=styles))
			else:
				_words_.append(word)
		return _words_
	def __assign_element_ids__(self, variable, key="element_id"):
		if isinstance(variable, list):
			dictionary = {}
			for i in variable: dictionary[i[key]] = i
			variable = dictionary
		elif isinstance(variable, dict):
			dictionary = {}
			for _, value in variable.items(): dictionary[value[key]] = value
			variable = dictionary
		else: raise ValueError(f"Unknown variable format: {variable}")
		return variable
		#

	# build docs from code.
	def build(self,
		# the package name.
		package=None,
		# the root path (optional).
		root=None,
		# the package's description (leave "" or None to ignore).
		description="",
		# the package's install command (leave "" or None to ignore).
		installation=None,
		# the package's installation description (leave "" or None to ignore).
		installation_description="",
		# include system functions (aka: def __somefunc__).
		system_functions=False,
		# include different path's or readme str.
		include=[],
		# banned sub paths.
		banned=[".docs/build.py"],
		# banned names.
		banned_names=["__main__.py", "utils.py"],
		# banned basenames.
		banned_basenames=["utils", "__pycache__", ".legacy"],
		# banned class types.
		banned_class_types=["Exception"],
		# the banned classes.
		banned_classes=[],
		# the banned functions.
		banned_functions=[],
		# the export path.
		readme=None,
		# the examples export path.
		examples=None, 
		# the chapters export path.
		chapters=None,
		# the replacemenets.
		replacements={},
	):	
		# funcs.
		def clean_params(params):
			clean = params.replace('(self)', '()').replace('self  ,', '').replace('self ,', '').replace('self,', '').replace("\n)", " )")
			while True:
				if clean[:len("( ")] == "( ":
					clean = "("+clean[2:]
				else: break
			return clean
		def build_description(info):
			description = info["description"]
			if description in [[], ""]:
				l = info['module']
				if l == None:
					l = info['name']
				if info["type"] == "class":
					description = f"The <attribute>{l}</attribute> object class."
				else:
					description = f"The <attribute>{l}</attribute> function."
			for from_, to_ in {
				"(required)":"",
				"(required)":"",
			}.items():
				description = description.replace(from_, to_)
			return description
		def build_params(info):
			parameters = []
			cleaned = clean_params(info["parameters"])
			param_name, param_number, param_format, param_value = None, None, None, None
			comments = ""
			required = False
			if cleaned != "()":
				dict_open = 0
				for line in cleaned[1:-1].split("\n"):
					for _ in range(100):
						if len(line) > 0 and line[0] == " ": line = line[1:]
						else: break
					new_open, new_closed = False, False
					for i in line:
						if i == "{": 
							if dict_open == 0: new_open = True
							dict_open += 1
						elif i == "}": 
							dict_open -= 1
							if dict_open == 0: new_closed = True
					if line not in ["", "}", "]", ")"] and (new_open or dict_open == 0) and not new_closed:
						if len(line) > 0 and line[0] == "#":
							comment = True
						else:
							comment = False
						if comment: 
							comments += line+"\n"
						else:
							# handle line / str.
							def handle(string, param_format=None, comments=""):
								if "=" in string:
									param_name = string.split("=")[0]
									param_value = string.split("=")[1].split(",")[0]
									required = "(required)" in comments or "(required)" in comments
								elif ":" in string:
									param_name = string.split(":")[0]
									required = True
									param_format = string.split(":")[1].split(",")[0]
								else:
									param_name = string.split(",")[0]
									required = True
									param_format = None
								return param_name, required, param_format
							# slice param format from comments.
							def parse_parameter_format_from_comments(param_format, comments=""):
								formats = ["None", "NoneType", "bool", "Boolean", "str", "String", "int", "Integer", "float", "dict", "Dictionary", "list", "Array", "ResponseObject", "OutputObject", "FilePath", "File", "Directory"]
								depth, last_sliced = 1, None
								for _ in range(100):
									sliced = String(comments).slice_tuple(depth=depth)[1:-1].replace(" ","").replace("	","").split(",")
									if sliced == last_sliced: break
									if len(sliced) > 0 and sliced[0] == "#":
										try: 
											param_number = int(sliced[1:])
										except:
											param_number = None
									for l_format in formats:
										if l_format in sliced:
											param_format = sliced
											break
									if param_format != None: break
									last_sliced = sliced
									depth += 1
								return param_format
							# slice param format from default value.
							def slice_param_format_from_default_value(param_format, param_value):
								if param_value in ["True", "False"]:
									param_format = ["bool"]
								elif len(param_value) > 0 and param_value[0] in ["'", '"']:
									param_format = ["str"]
								elif len(param_value) > 0 and param_value[0] in ["["]:
									param_format = ["list"]
								elif len(param_value) > 0 and param_value[0] in ["{"]:
									param_format = ["dict"]
								elif len(param_value) > 0 and param_value[0] in ["("]:
									param_format = ["slice"]
								elif param_value in ["dev0s.defaults.options.log_level"]:
									param_format = ["int"]
								else:
									if "." in str(param_value):
										try:
											float(param_value)
											param_format = ["float"]
										except: a=1
									else:
										try:
											int(param_value)
											param_format = ["int"]
										except: a=1
								return param_format, param_value
							# handle line.
							param_name, required, param_format = handle(line, param_format=param_format, comments=comments)
						if param_name != None:

							# slice param format from comments.
							if param_format == None:
								param_format = parse_parameter_format_from_comments(param_format, comments=comments)

							# slice param format from default value.
							if param_format == None and param_value not in [None,"None"]:
								param_format, param_value = slice_param_format_from_default_value(param_format, param_value)

							# unkown format.
							if param_format == None:
								param_format = "unknown"
								if "--hide-alerts" not in sys.argv:
									dev0s.response.log(f"Missing parameter format declaration from {info['type']} [{info['name']}] ({info['path']}).", mode="alert")
							if isinstance(param_format, (str,String)):
								param_format = [param_format]

							# create description from comments.
							param_description = []
							for line in comments.split("\n"):
								for _ in range(100):
									if len(line) > 0 and line[0] in ["#", " "]: line = line[1:]
									else: break
								if line not in [""]:
									param_description.append(str(String(line).capitalized_word()))

							# append.
							parameters.append(self.parameter(
								id=param_name,
								format=param_format,
								required=required,
								folded=not required,
								description=param_description,))

							# reset.
							param_name, param_number, param_format, param_value = None, None, None, None
							comments = ""
							required = False
			# exact copy to add remainders.
			if param_name != None:
				if param_format == None:
					formats = ["None", "NoneType", "bool", "Boolean", "str", "String", "int", "Integer", "float", "dict", "Dictionary", "list", "Array", "ResponseObject", "OutputObject", "FilePath", "File", "Directory"]
					depth, last_sliced = 1, None
					for _ in range(100):
						sliced = String(comments).slice_tuple(depth=depth)[1:-1].replace(" ","").replace("	","").split(",")
						if sliced == last_sliced: break
						if len(sliced) > 0 and sliced[0] == "#":
							try: 
								param_number = int(sliced[1:])
							except:
								param_number = None
						for l_format in formats:
							if l_format in sliced:
								param_format = sliced
								break
						if param_format != None: break
						last_sliced = sliced
						depth += 1
				if param_format == None and param_value not in [None,"None"]:
					if param_value in ["True", "False"]:
						param_format = ["bool"]
					elif len(param_value) > 0 and param_value[0] in ["'", '"']:
						param_format = ["str"]
					elif len(param_value) > 0 and param_value[0] in ["["]:
						param_format = ["list"]
					elif len(param_value) > 0 and param_value[0] in ["{"]:
						param_format = ["dict"]
					elif len(param_value) > 0 and param_value[0] in ["("]:
						param_format = ["slice"]
					elif param_value in ["dev0s.defaults.options.log_level"]:
						param_format = ["int"]
					else:
						if "." in str(param_value):
							try:
								float(param_value)
								param_format = ["float"]
							except: a=1
						else:
							try:
								int(param_value)
								param_format = ["int"]
							except: a=1
				if param_format == None:
					param_format = "unknown"
				if isinstance(param_format, (str,String)):
					param_format = [param_format]
				param_description = []
				for line in comments.split("\n"):
					for _ in range(100):
						if len(line) > 0 and line[0] in ["#", " "]: line = line[1:]
						else: break
					if line not in [""]:
						param_description.append(str(String(line).capitalized_word()))
				parameters.append(self.parameter(
					id=param_name,
					format=param_format,
					required=required,
					folded=not required,
					description=param_description,))
				param_name, param_number, param_format, param_value = None, None, None, None
				comments = ""
				required = False
			# end copy.
			return parameters
		def build_title(info, class_=None):
			if info["type"] in ["class"]:
				return info["raw_name"].split("-")[0]
			else:
				if class_ != None:
					return class_+"."+info["raw_name"].split("-")[0]
				else:
					return info["raw_name"].split("-")[0]
		def build_code(info):
			if info["type"] == "class":
				if "." in info["raw_name"]: l = info["raw_name"].split(".")[len(info["raw_name"].split("."))-1]
				else: l = info["raw_name"]
				initialized_name = String(l).variable_format()
				l = info["module"]
				if l == None: l = info["name"]
				if info["initialized"]:
					code = initialized_name+" = " + l
				else:
					# check if not a class without __init__
					if "self" not in info["parameters"]:
						code = initialized_name+" = " + l
					else:
						code = initialized_name+" = " + l + clean_params(str(info["parameters"]))
			elif info["type"] == "property":
				if "." in info["raw_name"]: l = info["raw_name"].split(".")[len(info["raw_name"].split("."))-1]
				else: l = info["raw_name"]
				initialized_name = String(l).variable_format()
				code = initialized_name+" = " + info["name"]
			else:
				code = info["return"]+" = " + info["name"] + clean_params(str(info["parameters"]))
			return code

		# vars.
		chapters_export = chapters
		chapters = []
		if installation_description in ["", None]: installation_description = ""
		if isinstance(installation_description, (str,String)): installation_description = [installation_description]
		# build code examples.
		docs, _ = Python(path=root).build_readme(
			# the package name.
			package=package,
			# the root path (optional).
			root=root,
			# the package's description (leave "" or None to ignore).
			description=description,
			# the package's install command (leave "" or None to ignore).
			installation=installation,
			# include system functions (aka: def __somefunc__).
			system_functions=system_functions,
			# include different path's or readme str.
			include=include,
			# banned sub paths.
			banned=banned,
			# banned names.
			banned_names=banned_names,
			# banned basenames.
			banned_basenames=banned_basenames,
			# banned class types.
			banned_class_types=banned_class_types,
			# the banned classes.
			banned_classes=banned_classes,
			# the banned functions.
			banned_functions=banned_functions,
			# the export path.
			readme=readme,
			# the examples export path.
			examples=examples, 
			# the replacements.
			replacements=replacements,)

		# loader.
		loader = Loader("Creating website chapters")
		
		# build installation chapter.
		sections = []
		if "inc-package-manager --install" in installation:
			sections += [
				# installation.
				self.section(
					title="Installation",
					description=[
						f"Easily install <italic>{package}</italic> with <italic>inc-package-manager</italic>.",
					],
					attributes=[],
					parameters=[],
					code_areas=[
						self.code_area(
							title="install",
							content={
								"cli":"""inc-package-manager --install vserver""",
								"bash":"""curl -X GET https://api.vandenberghinc.com/packages/download/\?package=vserver&api_key=***API_KEY*** -J -o ~/Downloads/vserver.zip """,
						}),
						
					]),
			]
		else:
			if installation_description == [""]:
				installation_description = [f"Install the {package} library."]
			sections += [
				# installation.
				self.section(
					title="Installation",
					description=installation_description,
					attributes=[],
					parameters=[],
					code_areas=[
						self.code_area(
							title="install",
							content={
								"bash":installation,
						}),
						
					]),
			]

		# append installation chapter.
		chapters.append(self.chapter(
			# the chapter title.
			title="Installation",
			# the chapter's sections.
			sections=sections,
			# whether the chapter is folded in the leftbar or not.
			folded=True,))

		# build code chapters.
		for chapter, items in docs.items():
			sections = []
			for id, info in items.items():

				# first indent functions.
				if info["type"].lower() == "function":

					# section.
					sections.append(self.section(
						title=build_title(info),
						description=build_description(info),
						attributes=[],
						parameters=build_params(info),
						code_areas=[
							self.code_area(
								title="func",
								content={
									"python":build_code(info),
								}
							),
						],
					))

				# object classes.
				elif info["type"].lower() == "class":

					# iterate properties.
					attributes = []
					for func_info in info["functions"]:
						if func_info["type"] in ["property"]:
							attributes.append(self.attribute(
								id=func_info["name"],
								format=func_info["return"],
								folded=True,
								description=func_info["description"],))

					# section.
					title = build_title(info)
					sections.append(self.section(
						title=title,
						description=build_description(info),
						attributes=attributes,
						parameters=build_params(info),
						code_areas=[
							self.code_area(
								title="init",
								content={
									"python":build_code(info),
								}
							),
						],
					))

					# iterate functions.
					for func_info in info["functions"]:
						if func_info["type"] not in ["property"] and "__init__" not in func_info["name"]:

							# func section.
							sections.append(self.subsection(
								title=build_title(func_info, class_=title),
								description=build_description(func_info),
								attributes=[],
								parameters=build_params(func_info),
								code_areas=[
									self.code_area(
										title="func",
										content={
											"python":build_code(func_info),
										}
									),
								],
							))

			# append chapter.
			chapters.append(self.chapter(
				# the chapter title.
				title=chapter,
				# the chapter's sections.
				sections=sections,
				# whether the chapter is folded in the leftbar or not.
				folded=True,))

		# save.
		if chapters_export != None:
			loader.mark(new_message=f"Saving created website docs [{chapters_export}].")
			Files.save(chapters_export, "chapters = "+str(chapters))
		loader.stop()


	#

# the documentation view.
class DocumentationView(View):
	# do not forget to add the template dir: FilePath(website.SOURCE_PATH).base(), in settings.py
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
		# the default chapter library.
		chapters=None,
		# insert specific colors (insert mode).
		colors={},
		# the w3bsite.Website object.
		website=None,
		# overwrite maintenance (bool) (leave None to use website.maintenance).
		maintenance=None,
	):

		# docs.
		DOCS = {
			"module":"website.views.DocumentationView", 
			"initialized":False,
			"description":[], 
			"chapter": "Views", }

		# defaults.
		View.__init__(self,
			base=base,
			id=id,
			url=url,
			html=html,
			landing_page=landing_page,
			website=website,
			# the view type.
			type="DocumentationView",)
		self.website = website
		self.maintenance_ = maintenance
		if self.maintenance_ == None: self.maintenance_ = self.website.maintenance

		# check library.
		if not Files.exists("__defaults__/static/media"): os.mkdir("__defaults__/static/media")
		if not Files.exists("__defaults__/static/media/docs"): os.system(f"cp -r {SOURCE_PATH}/classes/views/media/docs/ __defaults__/static/media/docs")

		# add template data.
		self.colors = {
			"white":"#FAFAFA",
			"light_white":"#E9F0FD",
			"grey":"#E5E5E5",
			"light_grey":"#D6D6D6",
			"dark_grey":"#424242",
			"blue":"#5A8FE6",
			"purple":"#323B83",#"#B32FCA",
			#"purple":"#9B00AA",
			"red":"#FD304E",
			"pink":"#F62B7D",
			"orange":"#FF8800",
			"green":"#006633",
			"darkest":"#1F2227",
			"darker": "#20242A",
			"dark": "#262B30",
			# background color.
			"topbar":"#FAFAFA",#1F2227", #"#FAFAFA",
			"background":"#323B83",#"#E7E9EF", #"#FAFAFA",
			"topbar_darkmode":"#1F2227",#1F2227", #"#FAFAFA",
			"background_darkmode":"#1F2227",#"#E7E9EF", #"#FAFAFA",
			# elements.
			"widgets":"#FAFAFA",
			"widgets_reversed":"#323B83",#"#1F2227",
			"widgets_darkmode":"#20242A",
			"widgets_reversed_darkmode":"#323B83",#"#1F2227",
			# text.
			"text":"#1F2227",
			"text_reversed":"#FAFAFA",
			"text_darkmode":"#FAFAFA",
			"text_reversed_darkmode":"#FAFAFA",
			# input & textareas.
			"input_txt":"#6C6B6D",
			"input_txt_reversed":"#FAFAFA",
			"input_bg":"#E9F0FD", #"#FAFAFA", 
			"input_bg_reversed":"#323B83",
			
			# buttons.
			"button_txt":"#FAFAFA",
			"button_txt_reversed":"#1F2227",
			"button_bg":"#323B83",
			"button_bg_reversed":"#FAFAFA",
			# custom colors.
			# ...
		}
		for key, value in colors.items(): self.colors[key] = value
		self.website.template_data = self.website.template({
			"COLORS":self.colors,
			"LEFTBAR_WIDTH":"250px",
		})

		# chapters.
		self.include_chapters(chapters)

		#
	def view(self, request):
		api_key = "your-api-key"
		response = self.website.users.authenticated(request)
		if response.success:
			response = self.website.users.get_api_key(email=response.email)
			if response.success: api_key = response.api_key
		if self.maintenance_: return self.maintenance(request)
		return self.render(request=request, html=f"w3bsite/classes/views/html/documentation_view.html", template_data={
			"API_KEY":api_key,
			"URL":self.url,
			"CHAPTERS":self.chapters,
		})
	def include_chapters(self, chapters, reset=True):
		if isinstance(chapters, (str, String, FilePath)):
			chapters = str(chapters)
			while True:
				if len(chapters) > 0 and chapters[0] == "/": chachapterspters = chapters[1:]
				elif len(chapters) > 0 and chapters[len(chapters)-1] == "/": chapters = chapters[:-1]
				else: break
			if not Files.exists(chapters):
				raise dev0s.exceptions.InvalidUsage(f"Specified DocumentationView chapters library {chapters} does not exist ({self.url}).")
			if reset: self.chapters = {}
			if os.path.isdir(chapters):
				replaced = (gfp.clean(chapters, remove_first_slash=True, remove_last_slash=True)+"/").replace('/','.').replace(".py", "")
				for path in Files.Directory(chapters).paths():
					id = self.__generate_element_id__("chapt_")
					name = FilePath(path).name().replace(".py", "")
					if ".py" in path:
						module = importlib.import_module(f"{replaced}{name}")
					module_chapters = module.chapters
					if isinstance(module_chapters, (list, Array)): # multiple chapters.
						return self.include_chapters(module_chapters, reset=False)
					elif isinstance(module_chapters, (dict, Dictionary)): # single chapter.
						self.chapters[id] = module_chapters
					else:
						raise dev0s.exceptions.InvalidUsage(f"<dev0s.views.docs.DocumentationView.include_chapters> Imported module chapters from [{chapters}] must be a (Dictionary, Array) not [{module_chapters.__class__.__name__}] ({self.url}).")
			else:
				replaced = gfp.clean(chapters, remove_first_slash=True, remove_last_slash=True).replace('/','.').replace(".py", "")
				name = FilePath(chapters).name().replace(".py", "")
				module = importlib.import_module(f"{replaced}")
				id = self.__generate_element_id__("chapt_")
				module_chapters = module.chapters
				if isinstance(module_chapters, (list, Array)): # multiple chapters.
					return self.include_chapters(module_chapters, reset=False)
				elif isinstance(module_chapters, (dict, Dictionary)): # single chapter.
					self.chapters[id] = module_chapters
				else:
					raise dev0s.exceptions.InvalidUsage(f"<dev0s.views.docs.DocumentationView.include_chapters> Imported module chapters from [{chapters}] must be a (Dictionary, Array) not [{module_chapters.__class__.__name__}] ({self.url}).")
		elif isinstance(chapters, (list, Array)):
			if reset: self.chapters = {}
			for item in chapters:
				self.chapters[item["element_id"]] = item
		elif isinstance(chapters, dict):
			if reset: 
				self.chapters = chapters
			else:
				self.chapters = Dictionary(self.chapters) + chapters
		elif isinstance(chapters, Dictionary):
			if reset: 
				self.chapters = chapters.dictionary
			else:
				self.chapters = Dictionary(self.chapters) + chapters.dictionary
		else:
			raise dev0s.exceptions.InvalidUsage(f"<dev0s.views.docs.DocumentationView.include_chapters> Parameter [chapters] must be a (String, FilePath, Dictionary, Array) not [{chapters.__class__.__name__}] ({self.url}).")
	def __generate_element_id__(self, joiner=""):
		return joiner+String().generate(length=32, digits=True, capitalize=True)
	

# initialized docs.
docs = Documentations()