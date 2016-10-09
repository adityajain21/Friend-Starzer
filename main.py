import os

from mechanize import Browser


br = Browser()

br.set_handle_robots(False)
br.set_handle_refresh(False)

br.open('https://github.com/login')

print list(br.forms())[0]

