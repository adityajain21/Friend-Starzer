import os, requests, json, getpass
from mechanize import Browser

br = Browser()

br.set_handle_robots(False)
br.set_handle_refresh(False)

br.open('https://github.com/login')

br.form=list(br.forms())[0]

_username = str(raw_input("Username for 'https://github.com': "))
_password = str(getpass.getpass("Password for 'https://" + _username + "@github.com': "))


email_control = br.form.find_control("login")
if email_control.type == "text":
	email_control.value = _username

password_control = br.form.find_control("password")
if password_control.type == "password":
	password_control.value = _password

for control in br.form.controls:
    submit = control

submit.readonly = False

if(br.submit().read().find('Sign in to GitHub')==-1):
	print("Logged in Succesfully.")
else:
	print ("Invalid Credentials. Please try again.")
	exit()


_friendusername = str(raw_input("Username of friend for which you want to star all the repos: "))

url = "https://api.github.com/users/" + _friendusername + "/repos"
response = requests.get(url)
data = json.loads(response.text)

for i in data:
	repo = i['name']
	url = "https://api.github.com/user/starred/" + _friendusername + "/" + repo
	if not i['fork']:
		print "The following repos are being starred: "
		print repo
		requests.put(url,auth=(_username,_password))
	

_reverse=str(raw_input("Do you want a reverse mechanism? (Y/N)  "))

if(_reverse == 'Y'):
	for i in data:
		repo = i['name']
		url = "https://api.github.com/user/starred/" + _friendusername + "/" + repo
		if not i['fork']:
			print "The following repos are being un-starred: "
			print repo
			requests.delete(url,auth=(_username,_password))

print "That was a great thing you did for your friend!"
