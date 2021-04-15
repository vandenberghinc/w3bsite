
// imports.
const execSync = require('child_process').execSync;
const { exec } = require("child_process");


// the utils object class.
class Utils {

	// init.
	constructor() {
		this.home = this.execute("echo $HOME").replaceAll("\n","")+"/"
		this.user = this.execute("echo $HOME").replaceAll("\n","")
	}

	// sleep delay.
	sleep(delay) {
		var start = new Date().getTime();
		while (new Date().getTime() < start + delay);
	}

	// execute bash/shell command.
	execute(command, encoding="utf-8") {
		const output = execSync(command, {encoding:encoding});  // the default is 'buffer'
		return output
	}

	// execute bash/shell command asynch.
	execute_async(command, handler) {
		exec(command, (error, stdout, stderr) => {
			if (error) {
				console.log(`error: ${error.message}`);
				handler(null, error)
				return;
			}
			if (stderr) {
				console.log(`stderr: ${stderr}`);
				handler(stderr, null)
				return;
			}
			console.log(`stdout: ${stdout}`);
			handler(stdout, null)
			return ;
		});
	}

}

// init the django object class.
const utils = new Utils();

// export the utils object class.
module.exports.utils = utils;

//