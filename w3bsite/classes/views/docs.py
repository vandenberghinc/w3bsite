
# imports
from w3bsite.classes.views.defaults import *

# the documentations object class.
import importlib
class Documentations(View):
	def __init__(self):
		a=1
	def chapter(self,
		# the chapter title.
		title="Chapter Title",
		# the chapter's sections.
		sections={},
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
		title="Section Title",
		description=None,
		attributes={},
		parameters={},
		code_areas={},
	):

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
			"element_id":self.__generate_element_id__(),
		}
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
		return self.__parameter_attribute__(
			id=id,
			format=format,
			description=self.__color_description__(description),
			required=required,
			folded=folded,)
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
		return self.__parameter_attribute__(
			id=id,
			format=format,
			description=self.__color_description__(description),
			folded=folded,)
	def code_area(self,
		# the header title.
		title="my_variable",
		# the header subtitle.
		substitle=None,
		# the code area's content.
		content={
			"json":{},
			"python":"",
			# use your own. Unkown types are just non colored strings.
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
					elif previous != None: raise ValueError(f"Unkown previous: {previous}")
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
					elif previous not in ["default",None]: raise ValueError(f"Unkown previous: {previous}")
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
				elif not isinstance(data, str): raise ValueError(f"Unkown json code area content format: {data}")
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
									slicer_id = utils.__first_occurence_reversed__(string=item, charset=[" ", "\n", "\r"])
									if slicer_id == None: slicer_id = " "
									before, after = utils.__before_after_last_occurence__(string=item, slicer=slicer_id, include_before=True)
									if len(after) > 0:
										words.append(self.__create_word__(word=before, joiner="", language=language))
									else:
										after = before
									if "." not in after:
										words.append(self.__create_word__(word=after[:-1], color="blue", joiner="", language=language))
										words.append(self.__create_word__(word="(", joiner="", language=language))
									else:
										before, after = utils.__before_after_last_occurence__(string=after, slicer=".", include_before=True)
										words.append(self.__create_word__(word=before, joiner="", language=language))
										words.append(self.__create_word__(word=after[:-1], color="blue", joiner="", language=language))
										words.append(self.__create_word__(word="(", joiner="", language=language))
								elif item == "...":
									words.append(self.__create_word__(word=item, color="orange", italic=True, joiner="", language=language))
								else:
									words.append(self.__create_word__(word=item, color="orange", italic=True, joiner="", language=language))
							else:
								before, after = utils.__before_after_first_occurence__(string=item, slicer="=", include=False)
								words.append(self.__create_word__(word=before, color="orange", italic=True, joiner="", language=language))
								words.append(self.__create_word__(word="=", color="red", joiner="", language=language))
								if "(" in after:
									if "." not in after:
										words.append(self.__create_word__(word=after[:-1], color="blue", joiner="", language=language))
										words.append(self.__create_word__(word="(", joiner="", language=language))
									else:
										before, after = utils.__before_after_last_occurence__(string=after, slicer=".", include_before=True)
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
						slicer_id = utils.__first_occurence_reversed__(string=chars, charset=[" ", "\n", "\r"]) 
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
										before, after_1 = utils.__before_after_last_occurence__(string=_chars_, slicer=".", include_before=True)
										first = utils.__first_occurence_reversed__(string=before, charset=[" string.", "\nstring."])
										if first != None:
											before, selected, after_2 = utils.__before_selected_after_first_occurence__(string=before, slicer="first")
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
								if last[str(len(i)+1)] not in [f" {int_chars}",f"\n{int_chars}",f"\r{int_chars}",f"({int_chars}",f"={int_chars}",f"+{int_chars}",f"-{int_chars}","{"+f"{int_chars}"]:
								#if lastchar not in [" ","\n","\r","(","=","+","-","{"]:
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
				elif not isinstance(data, str): raise ValueError(f"Unkown json code area content format: {data}")
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
	# system functions.
	def __parameter_attribute__(self,
		id="my_variable",
		format=None,
		description=None,
		required=False,
		folded=None,
	):
		if isinstance(format, str):
			format = [format]
		elif not isinstance(format, list):
			raise ValueError(f"Unkown format instance [{format}]. The format should be a list with formats or a single string format.")
		return {
			"id":id,
			"format":format,
			"description":description,
			"description_count":len(description),
			"folded":folded,
			"required":required,
			"element_id":self.__generate_element_id__(),
		}
	def __generate_element_id__(self, joiner=""):
		return joiner+Formats.String("").generate(length=32, digits=True, capitalize=True)
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
				word["value"], _ = utils.__before_after_last_occurence__(string=word["value"], slicer="<", include=False)
				styles = {}
				# append styles.
				block = False
				if not block and tag in ["<bold>"]:
					block = True
					styles = utils.__append_dict__(old=styles, overwrite=True, new={
						"font_weight":"700",})
				if not block and tag in ["<italic>"]:
					block = True
					styles = utils.__append_dict__(old=styles, overwrite=True, new={
						"font_style":"italic",})
				if not block and tag in ["<code>", "<parameter>", "<attribute>"]:
					styles = utils.__append_dict__(old=styles, overwrite=True, new={
						"background": f"#00000025", 
						"border":"1px solid #00000035",
						"border_radius":"10px",
						"font_family":"Courier New",
						"padding":"1.5px 7.5px 1.5px 7.5px",})
				if not block and tag in ["<parameter>", "<attribute>"]:
					styles = utils.__append_dict__(old=styles, overwrite=True, new={
						"font_style":"italic",})
				# append tagless word.
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
		else: raise ValueError(f"Unkown variable format: {variable}")
		return variable

# the documentation view.
class DocumentationView(View):
	# do not forget to add the template dir: Formats.FilePath(website.SOURCE_PATH).base(), in settings.py
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
		# the default chapter library.
		chapters=None,
		# insert specific colors (insert mode).
		colors={},
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

		# check library.
		if not os.path.exists("static/media"): os.mkdir("static/media")
		if not os.path.exists("static/media/docs"): os.system(f"cp -r {SOURCE_PATH}/classes/views/media/docs/ static/media/docs")

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
		for key, value in colors.items():self.colors[key] = value
		self.template_data["COLORS"] = self.colors
		self.template_data["colors"] = self.colors
		try:
			self.template_data["CHAPTERS"] = {}
		except KeyError:
			self.template_data["CHAPTERS"] = {}
		self.template_data["leftbar_width"] = "250px"

		# arguments.
		if chapters != None:
			while True:
				if len(chapters) > 0 and chapters[0] == "/": chapters = chapters[1:]
				elif len(chapters) > 0 and chapters[len(chapters)-1] == "/": chapters = chapters[:-1]
				else: break
			self.include_chapters(chapters)

		#
	def view(self, request):
		api_key = "your-api-key"
		response = self.website.users.authenticated(request)
		if response.success:
			response = self.website.users.get_api_key(email=response.email)
			if response.success: api_key = response.api_key
		template_data = dict(self.template_data)
		template_data["API_KEY"] = api_key
		template_data["URL"] = self.url
		template_data["CHAPTERS"] = self.chapters
		if self.website.maintenance: return self.maintenance(request)
		return render(request, f"{ALIAS}/classes/views/html/documentation_view.html", template_data)
	def include_chapters(self, chapters_library):
		if not os.path.exists(chapters_library):
			raise ValueError(f"Specified DocumentationView chapters library {chapters_library} does not exist.")
		self.chapters = {}
		if os.path.isdir(chapters_library):
			chapters_library += "/"
			replaced = chapters_library.replace('/','.').replace(".py", "")
			for path in Files.Directory(chapters_library).paths():
				id = self.__generate_element_id__("chapt_")
				name = Formats.FilePath(path).name().replace(".py", "")
				if ".py" in path:
					module = importlib.import_module(f"{replaced}{name}")
					self.chapters[id] = module.chapter
		else:
			replaced = chapters_library.replace('/','.').replace(".py", "")
			name = Formats.FilePath(chapters_library).name().replace(".py", "")
			module = importlib.import_module(f"{replaced}")
			id = self.__generate_element_id__("chapt_")
			self.chapters[id] = module.chapter
	def __generate_element_id__(self, joiner=""):
		return joiner+Formats.String("").generate(length=32, digits=True, capitalize=True)
	

# initialized docs.
docs = Documentations()