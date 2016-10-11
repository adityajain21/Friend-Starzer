import os
import requests
import json
import getpass
from mechanize import Browser


def check_credentials(username, password):
	br = Browser()

	br.set_handle_robots(False)
	br.set_handle_refresh(False)

	br.open('https://github.com/login')

	br.form = list(br.forms())[0]
	
	email_control = br.form.find_control("login")
	if email_control.type == "text":
		email_control.value = username

	password_control = br.form.find_control("password")
	if password_control.type == "password":
		password_control.value = password

	for control in br.form.controls:
		submit = control

	submit.readonly = False

	flag = br.submit().read().find('Sign in to GitHub')
	return flag == -1

def star_repo(username, password, friendusername, repo_list, mode):
	for repo in repo_list:
		repo_name = repo['name']
		url = "https://api.github.com/user/starred/" + friendusername + "/" + repo_name

		if not repo['fork']:
			print repo_name
			if mode:
				requests.put(url,auth=(username, password))
			else:
				requests.delete(url,auth=(username, password))


def main():
	_username = str(raw_input("Username for 'https://github.com': "))
	_password = str(getpass.getpass("Password for 'https://" + _username + "@github.com': "))

	if not check_credentials(_username, _password):
		print "Invalid Credentials. Please try again."
		return
	else:
		print "Logged in Succesfully."
		_friendusername = str(raw_input("Username of friend for which you want to star all the repos: "))
		
		url = "https://api.github.com/users/" + _friendusername + "/repos?per_page=100"
		response = requests.get(url)
		data = json.loads(response.text)
		
		print "\nThe following repos are being starred: "
		star_repo(_username, _password, _friendusername, data, True)

		_reverse = str(raw_input("\n\nDo you want a reverse mechanism? (Y/N) "))
		if(_reverse == 'Y'):
			print "\nThe following repos are being un-starred: "
			star_repo(_username, _password, _friendusername, data, False)

		print "\n\nThat was a great thing you did for your friend!"
		

if __name__ == "__main__":
	main()
