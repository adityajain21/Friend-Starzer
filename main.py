import os
import random
import time
from uuid import uuid4

from mechanize import Browser

br = Browser()

br.set_handle_robots(False)
br.set_handle_refresh(False)


br.open('https://github.com/login')

br.form=list(br.forms())[0]

_username = str(raw_input("Enter Username: "))
_password = str(raw_input("Enter password: "))

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