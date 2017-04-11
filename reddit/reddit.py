import requests
import requests.auth
import getpass

def get_auth_headers(api_id, api_password, user, password):
	client_auth = requests.auth.HTTPBasicAuth(api_id, api_password)

	post_data = {"grant_type" : "password", "username" : user, "password" : password}
	headers = {"User-Agent" : "RedditDownloaderPersonal by usamagaard"}
	response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)

	access_token = response.json().get('access_token')
	headers = {"Authorization" : "bearer " + access_token, "User-Agent" : "RedditDownloaderPersonal by usamagaard"}
	return headers
