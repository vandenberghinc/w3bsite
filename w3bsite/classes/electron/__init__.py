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
	def initialize(self):
		
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
			npm install electron --save -g
			npm install electron-packager --save -g
			npm install electron-installer-dmg --save-dev -g
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
		for path in Directory(build).paths(files_only=True, recursive=True):
			data, edits = Files.load(path), 0
			for from_, to_ in {
				"***DOMAIN***":self.domain,
				"***NAME***":self.name,
				"***ALIAS***":self.name.lower().replace("_","-").replace(" ","-"),
				"***AUTHOR***":self.author,
				"***DESCRIPTION***":self.description,
				"***VERSION***":self.version,
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
		response = self.build()
		if not response.success: return response
		build = response.build

		# logs.
		loader = Loader(f"Deploying electron app {self.name}.")

		# checks.
		dirs = [Files.join(self.root, ".electron"),]
		if "*" in os or "linux" in os:
			dirs += [Files.join(self.root, ".electron/.linux")]
		if "*" in os or "windows" in os:
			dirs += [Files.join(self.root, ".electron/.windows")]
		if "*" in os or "macos" in os:
			dirs += [Files.join(self.root, ".electron/.macos")]
		for dir in dirs:
			if not Files.exists(dir): Files.create(dir, directory=True)

		# check icons.
		img_base, img = Files.join(self.root, "__defaults__/static/"), None
		options = [Files.join(img_base, "favicon.png"), Files.join(img_base, "favicon.ico"), Files.join(img_base, "favicon.icns")]
		for i in options:
			if Files.exists(i): img = Image(path=i) ; break
		if img == None:
			return dev0s.response.error(f"No favicon exists at [{options[0]}].")
		for i in options:
			if not Files.exists(i): img.convert(i)

		# deploy.
		if "*" in os or "linux" in os:
			response = dev0s.code.execute(f"cd {build} && electron-packager . --overwrite --platform=darwin --arch=x64 --icon={img_base}/icon.icns --prune=true --out={self.root}/.electron/linux/")
			if not response.success: return response
		if "*" in os or "windows" in os:
			response = dev0s.code.execute(f"""cd {build} && electron-packager . {self.name} --overwrite --asar --platform=win32 --arch=ia32 --icon={img_base}/icon.ico --prune=true --out={self.root}/.electron/windows/ --version-string.CompanyName=CE --version-string.FileDescription=CE --version-string.ProductName="""+"""\""""+self.name+"""\" """)
			if not response.success: return response
		if "*" in os or "macos" in os:
			response = dev0s.code.execute(f"cd {build} && electron-packager . {self.name} --overwrite --asar --platform=linux --arch=x64 --icon={img_base}/icon.png --prune=true --out={self.root}/.electron/macos/")
			if not response.success: return response
			response = dev0s.code.execute(f"electron-installer-dmg {self.root}/.electron/macos/{self.name}.app {self.name} --out={self.root}/.electron/macos/ --overwrite --icon={img_base}/icon.icns")
			if not response.success: return response

		# handler.
		loader.stop()
		return dev0s.response.success(f"Successfully deployed electron app {self.name}.")

		#

	#

#