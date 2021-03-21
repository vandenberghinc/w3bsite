
// electron imports.
const electron = require('electron')
const { app, BrowserWindow } = require('electron')

// js imports.
const { utils } = require('./utils.js');
const { django } = require('./django.js');

// boot django when the app is ready.
app.whenReady().then(function() { django.boot() })

// kill the app when the user clode the app.
app.on('window-all-closed', () => {
	if (process.platform !== 'darwin') {
		app.quit()
	}
})

// macos: boot when icon in dock is clicked and there is no window opened.
app.on('activate', () => {
	if (BrowserWindow.getAllWindows().length === 0) {
		django.boot()
	}
})

//