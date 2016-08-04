#!/usr/bin/python

# try : 
# 	if os.fork() > 0 : 
# 		# parent
# os.system('touch /users/ironstein/desktop/abcde.txt && echo "running command" >> /users/ironstein/desktop/abcde.txt')
# command = "/Volumes/Macintosh\ HD/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
# command += " --remote-debugging-port=9222 --no-first-run --no-default-browser-check"
# command += " --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir') " + target_file
# os.system(command)
# print('command run')

import requests
response = requests.get('http://localhost:9222/json')

import webbrowser
w = webbrowser.get("/Volumes/Macintosh\ HD/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-default-browser-check --user-data-dir=$(mktemp -d -t %s")
w.open('http://google.co.in')