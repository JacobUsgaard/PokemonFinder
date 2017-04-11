import requests
import requests.auth
import urllib.request
import shutil
import re
import os
import stat
import reddit
import getpass

fileTypes = ('.jpg', '.gif', '.png')

def downloadImgurUrl(url):
	headers = {"Authorization" : "Client-ID 4a98896f357cc55"}

	match = re.match(r'.*imgur.com/a/(\w+)', url)
	if match:
		albumName = match.group(1)
		album = requests.get("https://api.imgur.com/3/album/" + albumName, headers=headers).json().get('data')

		if album is not None and album.get('images') is not None:
			[downloadUrl(image.get('link'), image.get('id')) for image in album.get('images')]
		return

	match = re.match(r'.*imgur.com/(\w+)', url)
	if match:
		imageName = match.group(1)
		image = requests.get("https://api.imgur.com/3/image/" + imageName, headers=headers).json().get('data')
		downloadUrl(image.get('link'), image.get('id'))
		return

def processListing(listing):
	url = listing.get('data').get('url')
	fileName = listing.get('data').get('id')

	if url.endswith(fileTypes):
		try:
			downloadUrl(url, fileName)
		except Exception as e:
			print('url: ' + url + ', file: ' + fileName + ', ' + repr(e))

	elif 'imgur.com' in url:
		downloadImgurUrl(url)

	else:
		print("Not processed: " + url)

def downloadUrl(url, fileName):
	if url is None:
		return

	print(url, end=" => ")

	match = re.match(r'.*(\.\w+)', url)
	if match:
		fileName += match.group(1)

	filePath = 'files/' + fileName
	if os.path.exists(filePath) and os.stat(filePath).st_size != 0:
		print("Already downloaded")
		return

	with urllib.request.urlopen(url) as response, open(filePath, 'wb') as downloadFile:
		print("Downloading...")
		shutil.copyfileobj(response, downloadFile)

api_user = r"MZI_IAuJlazyjw"
api_password = getpass.getpass(api_user + " password: ")

username = "usamagaard"
password = getpass.getpass(username + " password: ")

headers = reddit.get_auth_headers(api_user, api_password, username, password)

count=0
after=None
while count < 1:
	params = {"t" : "all", "count" : count, "after" : after}
	response = requests.get("https://oauth.reddit.com/r/WQHD_Wallpaper/top", headers=headers, params=params)

	data = response.json().get('data')
	children = data.get("children")
	[processListing(child) for child in children]

	count += len(children)
	after = data.get("after")
	print("count: " + str(count))
