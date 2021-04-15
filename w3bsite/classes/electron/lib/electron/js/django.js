
// imports.
const fs = require("fs")
const electron = require('electron')
const { app, BrowserWindow } = require('electron')
const { utils } = require('./utils.js');

// the django object class.
class Django {

	// init.
	constructor() {

		// settings.
		this.name = "***NAME***"
		this.alias = "***ALIAS***"
		this.domain = "***DOMAIN***"

		// must be set after import.
		this.win = null

		// sys attributes.
		this.__base__ = `${__filename}`.replace("/js/django.js", "/").replaceAll("//", "/")
		this.__running__ = false

	}

	// render an url.
	render_url(url) {
		url = "http://"+((url).replaceAll("https://","").replaceAll("http://","").replaceAll("//","/"))
		console.log("Rendering: "+url)
		this.win.loadURL(url);
	}

	// render a html file.
	render_html(path) {
		this.win.loadURL(`file://${path}`);
	}

	// execute javascript on the window.
	execute_js(code) {
		this.win.webContents.executeJavaScript(code)
	}

	// render the loader view.
	loader(message, hide=false) {

		// init.
		this.render_html(`${this.__base__}/html/loading.html`);
		if (hide == true) {
			this.execute_js(`
				document.getElementById("loader").style.display = "none"
			`)
		} else {
			this.execute_js(`
				document.getElementById("loader").style.display = "block"
			`)
		}
		this.execute_js(`
			document.getElementById("text").innerHTML = "`+message+`"
		`)
	}

	// check if venv is installed.
	venv(handler) {
		
		// check library.
		console.log("Checking library installation.")
		var __django__ = this

		// check venv.
		console.log("Library already installed.")
		console.log("Checking venv installation. ")
		fs.exists(`${utils.home}/.${__django__.alias}/venv`, function (exists) {

			// create venv.
			if (exists == false) {
				console.log("Venv not yet installed.")
				console.log(`Installing virtual environment [${utils.home}/.${__django__.alias}/venv]`)
				var output = utils.execute_async(`
					if [[ ! -d "${utils.home}/.${__django__.alias}" ]] ; then
						mkdir ${utils.home}/.${__django__.alias}
					fi
					python3 -m venv ${utils.home}/.${__django__.alias}/venv
					${utils.home}/.${__django__.alias}/venv/bin/python3 -m pip install -r ${__django__.__base__}/python/django/requirements/requirements.pip
				`, function(output, error) {

					// error.
					console.log("Encountered an error while creating the virtual environment.")
					console.log("Error: "+error)
					console.log("Output: "+output)
					if (error != null) {
						if (handler != null) {handler(false)}

					// venv created.
					} else {
						if (handler != null) {handler(true)}
					}
				})

			// library & venv installed.
			} else {
				console.log("Venv already installed.")
				if (handler != null) {handler(true)}
			}
		})

	}

	// check if django is already running.
	running(handler) {
		console.log(`curl -s ${this.domain}`)
		try {
			var output = utils.execute(`curl -s ${this.domain}`)
			var success = true
		} catch(e) {
			var success = false
		}
		if (success == false) {
			console.log('Django not yet running ...')
			this.__running__ = false
			if (handler != null) {handler(false)}
		} else {
			console.log('Django already running ...')
			this.__running__ = true
			if (handler != null) {handler(true)}
		}
	}

	// start the django webserver.
	start() {
		console.log("Starting django ...")
		if (process.platform == "darwin") {
			var executable =`/usr/bin/python3`
		} else {
			var executable =`${utils.home}/.${__django__.alias}/venv/bin/python3`
		}
		utils.execute_async(`cd ${this.__base__}/python/django && ${executable} ./__main__.py --w3bsite --start --developer`, function(output, error) {
			if (error != null) {
				console.log("Encountered an error while starting the webserver: "+error)
			} else {
				console.log("The webserver has finished running.\n"+output)
			}
		})
	}

	// wait till the webserver is running.
	await(handler, count=0) {
		console.log("Awaiting django ...")
		var __django__ = this
		try {
			utils.execute(`curl -s ${__django__.domain}`)
			var success = true
		} catch(e) {
			var success = false
		}
		if (success == true) {
			console.log('Starting django ... done')
			if (handler != null) {handler(true)}
		} else {
			count = count + 1
			if (count > 30) {
				console.log('Starting django ... failed')
				if (handler != null) {handler(false)}
			} else {
				setTimeout(function() {
					__django__.await(handler, count)
				}, 1500)
			}
		}
	}

	// render django when the webserver is running.
	render(reattempt=true) {

		// render url.
		var __django__ = this

		// loop.
		try {
			utils.execute(`curl -s ${__django__.domain}/accounts/login/`)
			var url = `${__django__.domain}/accounts/login/?next=/&electron=true`
		} catch(e) {
			var url = `${__django__.domain}/?electron=true`
		}
		this.render_url(url)

		// failed to render.
		this.win.webContents.on('did-fail-load', ()=>{
			if (reattempt == true) {
				console.log("Rendering failed ==> reattempting.")
				__django__.render(false)
			} else {
				console.log("Rendering failed == stop rendering.")
			}
		});

		// successfull render.
		this.win.webContents.on('did-finish-load', ()=>{
			console.log("Rendering successfull.")
		});
	}

	// boot the django webserver. 
	boot() {

		// windows.
		if (this.win == null) {
			this.win = new BrowserWindow({
				width: 1000,
				height: 800,
				minWidth: 400,
				minHeight: 500,
				webPreferences: {
					nodeIntegration: false // with true js from website fails.
				},
				titleBarStyle: 'hidden',
				//icon: "https://poker-stats-app.herokuapp.com/static/media/pokerstats/app_icon.png",
			})
		}

		// developer tools.
		//this.win.webContents.openDevTools()


		// loader.
		this.loader(`Starting ${this.name}`)

		// copy vars.
		var __django__ = this

		// check venv installed.
		this.venv(function(installed) {

			// successfully installed or already installed.
			if (installed == true) {

				// check if django already running.
				__django__.loader("Starting "+__django__.name)
				__django__.running(function(running) {

					// django not yet running.
					if (running == false) {

						// start django.
						__django__.start()  
						__django__.await(function(running) {

							// successfully started.
							utils.sleep(1000)
							if (running == true ) {
								console.log("Successfully started the django webserver.")
								__django__.render()

							// failed to start.
							} else {
								__django__.loader(`Failed to start ${__django__.name}.`, true)
							}
						})

					// django already running.
					} else {
						console.log("Django already running.")
						__django__.render()

					}
				})
			
			// failed to install.
			} else {
				__django__.loader(`Failed to install the ${__django__.name} virtual environment.`, true)

			}
		})
	}

	// main electron function.

}

// init the django object class.
const django = new Django();

// export the djang object class.
module.exports.django = django;

//