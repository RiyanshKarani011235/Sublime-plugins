import sublime, sublime_plugin
import os
import sys

working_directory_list = __file__.split('/')[:-1]
working_directory = ''
for element in working_directory_list : 
	working_directory += element + '/'
sys.path.append(working_directory)

import json
import requests
import websocket
import requests

class IpythonNotebookCodeSyncUtilityCommand(sublime_plugin.TextCommand):

	def run(self,edit) : 
		target_ipynb_files = self.get_matching_ipynb_files() 
		if target_ipynb_files != [] : 
			print('we have a match -> \n' + str(target_ipynb_files))  
		else : 
			print('no matching file found')
			return None
			# exit code

		# creating a line list of the calling file once, to be 
		# passed to the create_new_ipython_notebook method
		file_to_be_copied = []
		with open(self.view.file_name(),'r') as file:
			for line in file : 
				file_to_be_copied.append(line)
		
		new_file_to_be_copied = []
		for line in file_to_be_copied : 
			new_line = ''
			for character in line : 
				if character == '\t' : 
					new_line += '    '
				elif character == '"' :
					new_line += '\\"'
				else : 
					new_line += character
			new_file_to_be_copied.append(new_line)

		file_to_be_copied = new_file_to_be_copied
		del(new_file_to_be_copied)

		for target_ipynb_file in target_ipynb_files :
			self.edit_new_ipython_notebook(file_to_be_copied,target_ipynb_file)

		refresh_json = json.dumps({
			"id": 0,
			"method": "Page.reload",
			"params": { "ignoreCache": True }
		})

		try : 
			response = requests.get('http://localhost:9222/json')
		except : 
			print('connection error. Did you start chrome in the remote debugging mode?')
			return
		for page in response.json() : 
			if 'localhost:888' in page['url'] : 
				print(page['url'])
				ws = websocket.create_connection(page['webSocketDebuggerUrl'])
				ws.send(refresh_json)
				ws.close()


	def get_matching_ipynb_files(self):
		all_filenames = self.get_all_filenames()
		ipynb_filenames = []
		target_ipynb_files = []

		for filename in all_filenames : 
			if filename.split('.')[-1] == 'ipynb' : 
				ipynb_filenames.append(filename)

		for ipynb_filename in ipynb_filenames : 
			
			# don't want to change the checkpoint file, ipython will do it for us
			if '.ipynb_checkpoints/' not in ipynb_filename :
				# checking if the ipynb file contains the code for the calling file	
				with open(ipynb_filename,'r') as file : 
					if ('%%file ' + self.view.file_name().split('/')[-1]) in file.read() : 
						target_ipynb_files.append(ipynb_filename)

		return target_ipynb_files

	def getcwd(self) : 
		working_directory = ''
		for element in self.view.file_name().split('/')[:-1] : 
			working_directory += element + '/'
		return working_directory

	def get_all_filenames(self) : 
		all_filenames = []
		for root,dirs,files in os.walk(self.getcwd()) :
			for file in files : 
				if root[-1] != '/' :
					all_filenames.append(root + '/' + file)
				else : 
					all_filenames.append(root + file)
		return all_filenames

	def edit_new_ipython_notebook(self,file_to_be_copied,target_ipynb_file) :

		ipynb_file = []
		with open(target_ipynb_file,'r') as file : 
			for line in file : 
				ipynb_file.append(line)

		i = 0
		while i < len(ipynb_file) :
			
			if ('%%file ' + self.view.file_name().split('/')[-1]) in ipynb_file[i] :
				j = i
				# when the source string is complete, there is a line with 
				# just ']' nothing else
				# I use this to detect the end of source
				while '"' in ipynb_file[j] : 
					j += 1
				print(j)

				# remove all the written code first
				for k in range(i+1,j) : 
					print('popping - ' + ipynb_file[i+1])
					ipynb_file.pop(i+1)


				# add the new code
				for k in range(len(file_to_be_copied)) :
					ipynb_file.insert(i+k+1,'    "' + file_to_be_copied[k][:-1] + '\\n",\n')

				ipynb_file[i+k+1] = ipynb_file[i+k+1][:-5] + '"\n'

				i = i + k + 1
			i += 1

		ipynb_file_string = ''
		for line in ipynb_file : 
			ipynb_file_string += line

		with open(target_ipynb_file,'w') as file : 
			file.write(ipynb_file_string)

