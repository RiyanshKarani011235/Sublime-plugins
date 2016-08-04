import sublime, sublime_plugin
import os
import sys
import json
import requests
import websocket
import requests
import time
import webbrowser

log_file = '/users/ironstein/desktop/abcde.txt'

class ChromeHtmlCodeSyncUtilityCommand(sublime_plugin.TextCommand):

	def run(self,edit) : 
		print('running ChromeHtmlCodeSyncUtilityCommand')
		target_file = self.view.file_name()
		refresh_json = json.dumps({
			"id": 0,
			"method": "Page.reload",
			"params": { "ignoreCache": True }
		})

		try : 
			response = requests.get('http://localhost:9222/json')
		except : 
			self.open_google_chrome(target_file)
		else : 
			for page in response.json() : 
				if target_file in page['url'] : 
					print(page['url'])
					ws = websocket.create_connection(page['webSocketDebuggerUrl'])
					ws.send(refresh_json)
					ws.close()
					return
			w = webbrowser.get("/Volumes/Macintosh\ HD/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --no-first-run")
			w.open('file://' + target_file)

	def open_google_chrome(self, filename) : 
		try : 
			if os.fork() > 0 : 
				print('this is the parent')
				# parent process
				return True
		except OSError as e: 
			print('fork 1 failed')
			return False
		
		print('this is the child')

		os.chdir('/')
		os.umask(0)
		os.setsid()  # the child process is now the session leader

		try :
			if os.fork() > 0 : 
				raise SystemExit(0)
		except OSError as e: 
			os.system('echo "fork 2 failed" >> ' + log_file)
			raise RuntimeError()
		else : 
			os.system('touch /users/ironstein/desktop/abcde.txt && echo "running command" >> ' + log_file)
			command = "/Volumes/Macintosh\ HD/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome"
			command += " --remote-debugging-port=9222 --no-first-run --no-default-browser-check"
			command += " --user-data-dir=$(mktemp -d -t 'chrome-remote_data_dir') " + filename
			os.system(command)
			os.system('echo exiting >> ' + log_file)
			raise SystemExit(0)