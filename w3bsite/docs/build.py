#!/usr/bin/env python3

# imports.
import sys
from fil3s import *

# settings.
root = gfp.base(path=__file__, back=2)
docs = Files.join(root, "docs", "/")
name = gfp.name(path=root)

# export.
if "--overwrite" in sys.argv:
	readme = Files.join(root, "README.md")
	export = None
else:
	readme = Files.join(docs, "docs.md")
	export = Files.join(docs, "examples.md")

# build readme.
Python(path=root).build_readme(
	# the package name.
	package=name,
	# the package's description (leave "" or None to ignore).
	description="Some description.",
	# the package's install command (leave "" or None to ignore).
	installation=f"curl -s https://raw.githubusercontent.com/vandenberghinc/{name}/master/{name}/requirements/installer.remote | bash ",
	# include system functions (aka: def __somefunc__).
	system_functions=False,
	# include different path's or readme str.
	include=[Files.join(docs, "additional.md")],
	# banned sub paths.
	banned=["docs/build.py"],
	# banned names.
	banned_names=["__main__.py", "utils.py", "daemons.py", "index.py", ".version.py"],
	# banned basenames.
	banned_basenames=["utils", "__pycache__", ".legacy", "webserver"],
	# banned class types.
	banned_class_types=["Exception"],
	# the banned classes.
	banned_classes=["Daemon", "Clients"],
	# the banned functions.
	banned_functions=["daemon"],
	# the export path.
	readme=readme,
	# the examples export path.
	examples=export,
)