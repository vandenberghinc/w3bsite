#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from w3bsite.classes.config import *

# the main website class.
class Electron(Object):
	def __init__(self, attributes={}):

		# defaults.
		Object.__init__(self, traceback="website.electron")
		self.assign(attributes)

		# attributes.
		self.lib = Directory(f"{SOURCE_PATH}/classes/electron/lib/")

		# sys attributes.
		self.__initialized__ = False

		#

	# initialize electron.
	def initialize(self, build=None):
		
		# install npm & dependencies.
		loader = Loader(f"Initializing electron")
		response = dev0s.code.execute(f"""
			if [[ "$OSTYPE" =~ "darwin" ]] ; then
				if ! command -v "brew" &> /dev/null ; then
					printf "\n" | /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
				fi
				if ! command -v "npm" &> /dev/null ; then
					brew install npm
				fi
			else
				if ! command -v "npm" &> /dev/null ; then
					echo "Error: npm is not installed. Install npm on your current machine to deploy app electron {self.name}."
					exit 1
				fi
			fi
			build="{build}"
			if [[ "$build" != "None" ]] ; then
				cd $build
			fi
			npm install electron --save {Boolean(build == None).string(true='-g', false='')}
			npm install electron-packager --save {Boolean(build == None).string(true='-g', false='')}
			npm install electron-installer-dmg --save-dev {Boolean(build == None).string(true='-g', false='')}
		""")
		if not response.success: 
			loader.stop(success=False)
			return response

		# handler.
		self.__initialized__ = True
		loader.stop()
		return dev0s.response.success(f"Successfully initialized {self.traceback}.")

	# build the electron source code.
	def build(self,
		# the export build path (str, FilePath) (optional).
		build=None,
		# install the node modules.
		node_modules=False,
	):

		# check initialized.
		if not self.__initialized__:
			response = self.initialize()
			if not response.success: return response

		# create electron source code.
		loader = Loader(f"Building electron app {self.name}.")
		if build == None: build = f"/tmp/{self.name}.electron/"
		else: build = str(build)
		Files.delete(build, forced=True)
		Files.copy(self.lib.join("electron"), build, exclude=[
			".git",
			".gitignore",
			".gitattributes",
			".electron",
		])
		include = [
			"html/*",
            "js/*",
            "python/*"
		]
		root = Directory(self.root)
		for dir in root.paths(recursive=True, dirs_only=True, banned_names=[".git", ".gitignore", ".gitattributes", ".electron", ".docs", ]):
			dir = gfp.clean(f"python/django/{root.subpath(dir)}/*")
			if dev0s.defaults.options.log_level >= 1:
				dev0s.response.log("Include directory "+dir)
			include.append(dir)
		include = json.dumps(include, indent=0, ensure_ascii=False)
		for path in Directory(build).paths(files_only=True, recursive=True):
			data, edits = Files.load(path), 0
			for from_, to_ in {
				"***DOMAIN***":self.domain,
				"***NAME***":self.name,
				"***ALIAS***":self.name.lower().replace("_","-").replace(" ","-"),
				"***AUTHOR***":self.author,
				"***DESCRIPTION***":self.description,
				"***VERSION***":self.version,
				"***INCLUDE***":include,
			}.items(): 
				if from_ in data: 
					edits += 1
					data = data.replace(str(from_), str(to_))
			if edits > 0:
				Files.save(path, data)

		# copy django into electron.
		Files.copy(self.root, Files.join(build, "python/django/"), exclude=[
			".git",
			".gitignore",
			".gitattributes",
			".electron",
		])

		# install node modules.
		if node_modules:
			response = self.initialize(build=build)
			if not response.success: return response

		# handler.
		loader.stop()
		return dev0s.response.success(f"Successfully deployed electron app {self.name}.", {
			"build":build,
		})

		#

	# developer start the electron app.
	def start(self):

		# build source code.
		response = self.build()
		if not response.success: return response
		build = response.build
		loader = Loader(f"Starting electron app {self.name}")

		# refresh source code thread.
		class Refresh(Thread):
			def __init__(self, attributes={}):
				Thread.__init__(self)
				self.assign(attributes)
			def __run__(self):
				while self.run_permission:
					Files.copy(self.root, Files.join(self.build, "python/django/"), exclude=[
						".git",
						".gitignore",
						".gitattributes",
						".electron",
					])
					if not response.success: response.crash()
					time.sleep(5)
				return dev0s.response.success("Successfully stopped the daemon")

		# run electron thread.
		class Run(Thread):
			def __init__(self, attributes={}):
				Thread.__init__(self)
				self.assign(attributes)
			def __run__(self):
				
				# start.
				response = dev0s.code.execute(f"cd {build} && electron .", async_=True)
				if not response.success: return response
				self.process = response.process
				self.process.log_level = 0

				# read.
				while self.process.running:
					response = self.process.read(wait=False)
					if not response.success: return response
					if len(response.new_output) > 0 and response.new_output[len(response.new_output)-1] == "\n": response.new_output = response.new_output[:-1]
					if response.new_output not in [""]: print(response.new_output)
					if not self.run_permission: break

				# stop.
				response = self.process.kill()
				if not response.success: return response
				return dev0s.response.success("Successfully stopped electron.")

				#
		
		# objects.
		attributes = {
			"root":gfp.clean(self.root, remove_last_slash=True)+"/",
			"build":gfp.clean(build, remove_last_slash=True)+"/",
		}
		refresh = Refresh(attributes)
		run = Run(attributes)

		# start.
		loader.stop()
		response = run.safe_start()
		if not response.success: return response
		response = refresh.safe_start()
		if not response.success: return response

		# sleep.
		while True:
			try:
				time.sleep(60)
			except: break

		# stop.
		response = run.safe_stop()
		if not response.success: return response
		response = refresh.safe_stop()
		if not response.success: return response

		# handler.
		return dev0s.response.success(f"Successfully stopped electron app {self.name}.")

		#

	# deploy the electron app.
	def deploy(self,
		# the target operating system (list) [linux, macos, windows].
		os=["macos"],
	):

		# build source code.
		response = self.build(node_modules=True)
		if not response.success: return response
		build = response.build

		# logs.
		loader = Loader(f"Deploying electron app {self.name}.")

		# checks.
		dirs = [Files.join(self.root, ".electron"),]
		if "*" in os or "linux" in os:
			dirs += [Files.join(self.root, ".electron/linux")]
		if "*" in os or "windows" in os:
			dirs += [Files.join(self.root, ".electron/windows")]
		if "*" in os or "macos" in os:
			dirs += [Files.join(self.root, ".electron/macos")]
		for dir in dirs:
			if not Files.exists(dir): Files.create(dir, directory=True)

		# check icons.
		img_base, img = Files.join(self.root, "__defaults__/static/"), None
		options = [Files.join(img_base, "favicon.png"), Files.join(img_base, "favicon.ico"), Files.join(img_base, "favicon.icns")]
		for i in options:
			if Files.exists(i): img = Image(path=i) ; break
		if img == None:
			loader.stop(success=False)
			return dev0s.response.error(f"No favicon exists at [{options[0]}].")
		for i in options:
			if not Files.exists(i): img.convert(i)

		# deploy.
		tmp_build = Directory("/tmp/build/")
		if "*" in os or "macos" in os:
			destination = Files.join(self.root, f".electron/macos/{self.name}")
			img = f"{img_base}/favicon.icns"
			if not Files.exists(img):
				loader.stop(success=False)
				return dev0s.response.error(f"Icon file [{img}] does not exist.")
			#Files.delete(destination, forced=True)
			tmp_build.fp.delete(forced=True)
			tmp_build.fp.create(directory=True)
			response = dev0s.code.execute(f"cd {build} && electron-packager . --overwrite --platform=darwin --arch=x64 --icon={img} --prune=true --out={tmp_build}")
			if not response.success: 
				loader.stop(success=False)
				return response
			print(tmp_build.paths()[0])
			loader.stop()
			quit()
			Files.mode(tmp_build.paths()[0], destination)
			"""
			response = dev0s.code.execute(f"electron-installer-dmg {self.root}/.electron/macos/{self.name}.app {self.name} --out={tmp_build} --overwrite --icon={img}")
			if not response.success: 
				loader.stop(success=False)
				return response
			destination = Files.join(self.root, f".electron/macos/{self.name}.dmg")
			Files.delete(destination, forced=True)
			Files.move(tmp_build.paths()[0], destination)
			"""
		if "*" in os or "windows" in os:
			destination = Files.join(self.root, f".electron/windows/{self.name}")
			img = f"{img_base}/favicon.ico"
			if not Files.exists(img):
				loader.stop(success=False)
				return dev0s.response.error(f"Icon file [{img}] does not exist.")
			Files.delete(destination, forced=True)
			tmp_build.fp.delete(forced=True)
			tmp_build.fp.create(directory=True)
			response = dev0s.code.execute(f"""cd {build} && electron-packager . {self.name} --overwrite --asar --platform=win32 --arch=ia32 --icon={img} --prune=true --out={tmp_build} --version-string.CompanyName=CE --version-string.FileDescription=CE --version-string.ProductName="""+"""\""""+self.name+"""\" """)
			if not response.success: 
				loader.stop(success=False)
				return response
			Files.move(tmp_build.paths()[0], destination)
		if "*" in os or "linux" in os:
			destination = Files.join(self.root, f".electron/linux/{self.name}")
			img = f"{img_base}/favicon.png"
			if not Files.exists(img):
				loader.stop(success=False)
				return dev0s.response.error(f"Icon file [{img}] does not exist.")
			Files.delete(destination, forced=True)
			tmp_build.fp.delete(forced=True)
			tmp_build.fp.create(directory=True)
			response = dev0s.code.execute(f"cd {build} && electron-packager . {self.name} --overwrite --asar --platform=linux --arch=x64 --icon={img} --prune=true --out={tmp_build}")
			if not response.success: 
				loader.stop(success=False)
				return response
			Files.move(tmp_build.paths()[0], destination)

		# handler.
		loader.stop()
		return dev0s.response.success(f"Successfully deployed electron app {self.name}.")

		#

	#

#
