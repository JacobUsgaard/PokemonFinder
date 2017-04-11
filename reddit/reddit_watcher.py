import requests
import requests.auth
import reddit
import smtplib
import getpass
import time
import sys
import os
import daemon
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

email_user = "reddit.downloader@gmail.com"
email_password = getpass.getpass(email_user + " password: ")

api_user = r"MZI_IAuJlazyjw"
api_password = getpass.getpass(api_user + " password: ")

username = "usamagaard"
password = getpass.getpass(username + " password: ")

def find_listing_by_id(posting_id):
	file_name = '/home/ubuntu/python/reddit/db/db.txt'
	with open(file_name, 'r') as db:
		lines = db.readlines()

	for line in lines:
		if line.strip('\n') == str(posting_id):
			return True

	with open(file_name, 'a') as db:
		db.write(str(posting_id) + '\n')
	return False

def email_listing(data):
	title = data.get('title')
	url = 'https://reddit.com' + data.get('permalink')

	message = EmailMessage()
	message['Subject'] = "New Posting"
	
	content = title + "\n" + url
	print(content)
	message.set_content(content)
	
	message['To'] = 'goose4523@gmail.com'
	message['From'] = email_user

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(email_user, email_password)
	server.send_message(message)
	server.close()

def check_new():
	headers = reddit.get_auth_headers(api_user, api_password, username, password)

	params = { 'limit' : 25 }
	response = requests.get('https://oauth.reddit.com/r/PokemonGoMPLS/new', headers=headers, params=params)

	data = response.json().get('data')
	children = data.get("children")

	for child in children:
		data = child.get('data')
		if not find_listing_by_id(data.get('id')):
			email_listing(data)
		else
			return

def worker():
	while(True):
		try:
			check_new()
		except Exception as e:
			sys.stderr.write('{0}'.format(e))
		time.sleep(60)

daemon.daemonize('/home/ubuntu/python/reddit/log/log.in', '/home/ubuntu/python/reddit/log/log.out', '/home/ubuntu/python/reddit/log/log.err')
worker()
