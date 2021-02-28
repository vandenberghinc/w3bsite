
# CLI Usage:
	Usage: ssht00ls <mode> <options> 
	Modes:
	    --create-alias : Create a ssh alias.
	        --server myserver : Specify the server's name.
	        --username myuser : Specify the username.
	        --ip 0.0.0.0 : Specify the server's ip.
	        --port 22 : Specify the server's port.
	        for ssh keys::
	        --key /path/to/key/private_key : Specify the path to the private key.
	        --passphrase 'MyPassphrase123' : Specify the keys pasphrase (optional).
	        for smart cards::
	        --smart-cards : Enable the smart cards boolean.
	        --pin 123456 : Specify the smart cards pin code (optional).
	    --generate : Generate a ssh key.
	        --path /keys/mykey/ : Specify the keys directory path.
	        --passphrase Passphrase123 : Specify the keys passphrase.
	        --comment 'My Key' : Specify the keys comment.
	    --command <alias> 'ls .' : Execute a command over ssh.
	    --session <alias> : Start a ssh session.
	        --options ''  : Specify additional ssh options (optional).
	    --pull <path> <alias>:<remote> : Pull a file / directory.
	        --delete : Also update the deleted files (optional).
	        --safe : Enable version control.
	        --forced : Enable forced mode.
	    --push <alias>:<remote> <path> : Push a file / directory.
	    --mount <alias>:<remote> <path> : Mount a remote directory.
	    --unmount <path> : Unmount a mounted remote directory.
	        --sudo : Root permission required.
	    --index <path> / <alias>:<remote> : Index the specified path / alias:remote.
	    --start-agent : Start the ssht00ls agent.
	    --stop-agent : Stop the ssht00ls agent.
	    --start-daemon <alias>:<remote> <path> : Start a ssync daemon.
	    --stop-daemon <path> : Stop a ssync daemon.
	    --kill <identifier> : Kill all ssh processes that include the identifier.
	    --config : Edit the ssht00ls configuration file (nano).
	    -h / --help : Show the documentation.
	Options:
	    -j / --json : Print the response in json format.
	Notes:
	    SSHT00LS_CONFIG : Specify the $SSHT00LS_CONFIG environment variable to use a different ssht00ls config file.
	Author: Daan van den Bergh. 
	Copyright: © Daan van den Bergh 2021. All rights reserved.
