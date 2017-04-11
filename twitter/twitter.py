import requests
import requests.auth
import base64
import logging
import getpass
import smtplib
import sys
import time
import daemon
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

email_user = r"reddit.downloader@gmail.com"
email_password = getpass.getpass(email_user + " password:")

key = "8MplWHpWhuaWOpJyPjs5oLEDW"
secret = getpass.getpass(key + " password:")

file_name = "/home/ubuntu/python/twitter/db/db.txt"

since_id = 1

def start_logging():
	import http.client as http_client
	http_client.HTTPConnection.debuglevel = 1

	# You must initialize logging, otherwise you'll not see debug output.
	logging.basicConfig()
	logging.getLogger().setLevel(logging.DEBUG)
	requests_log = logging.getLogger("requests.packages.urllib3")
	requests_log.setLevel(logging.DEBUG)
	requests_log.propagate = True

def get_auth_headers():
	basic = "Basic " + base64.b64encode((key + ":" + secret).encode("utf-8")).decode("utf-8")
	headers = {"Authorization" : basic, "Content-Type" : "application/x-www-form-urlencoded;charset=UTF-8", "User-Agent" : "usamagaard twitter"}

	post_data = "grant_type=client_credentials"

	response = requests.post("https://api.twitter.com/oauth2/token", data=post_data, headers=headers)

	access_token = response.json().get("access_token")
	headers = {"Authorization" : "Bearer " + access_token, "User-Agent" : "usamagaard twitter"}

	return headers

def check_new():
	headers = get_auth_headers()

	global since_id
	params = {"count" : "25", "trim_user" : "true", "exclude_replies" : "true", "include_rts" : "true", "screen_name" : "jdoughberg33333", "since_id" : since_id}

	response = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json", headers=headers, params=params)

	tweets = response.json()

	for tweet in tweets:
		object_id = tweet.get("id")
		since_id = max(int(float(object_id)), since_id)
		if not find_by_id(object_id, file_name):
			if find_by_name(tweet.get("text"), "/home/ubuntu/python/twitter/log/log.in"):
				email_object(tweet)

			with open(file_name, 'a') as db:
				db.write(str(object_id) + '\n')
		else:
			return

def find_by_name(name, file_name):
	with open(file_name, 'r') as db:
		lines = db.readlines()
	for line in lines:
		if line.strip('\n').lower() in str(name).lower():
			return True

	return False

def email_object(tweet):
	title = tweet.get("text")

	print(title)

	message = EmailMessage()
	message["Subject"] = "New Tweet"

	message.set_content(title)

	message["To"] = "goose4523@gmail.com"
	message["From"] = email_user

	server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
	server.ehlo()
	server.login(email_user, email_password)
	server.send_message(message)
	server.close()

def find_by_id(object_id, file_name):
	with open(file_name, 'r') as db:
		lines = db.readlines()

	for line in lines:
		if line.strip('\n') == str(object_id):
			return True

	return False

daemon.daemonize('/home/ubuntu/python/twitter/log/log.in', '/home/ubuntu/python/twitter/log/log.out', '/home/ubuntu/python/twitter/log/log.err')

while True:
	try:
		check_new()
	except Exception as e:
		sys.stderr.write("{0}".format(e))
	
	time.sleep(60)
