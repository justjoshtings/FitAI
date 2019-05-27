'''
Establish initial connection to gain access and refresh token from Fitbit API
'''

'''
Import tools
'''
import requests
from requests_oauthlib import OAuth2Session
import json
import credentials as cred
import base64


class FitbitAuthorization:
	def __init__(self, clientID, clientSecret, callback_URL):
		self.clientID = clientID 
		self.clientSecret = clientSecret
		self.callback_URL = callback_URL
		self.authorization_URI = 'https://www.fitbit.com/oauth2/authorize'
		self.token_request_URI = 'https://api.fitbit.com/oauth2/token'
		self.client_encode = base64.b64encode((self.clientID+':'+self.clientSecret).encode()).decode('utf-8')
		self.scope = [
	            "activity",
	            "nutrition",
	            "heartrate",
	            "location",
	            "nutrition",
	            "profile",
	            "settings",
	            "sleep",
	            "social",
	            "weight",]


	def establishConnection(self):
		'''
		Establish OAuthorization connection with Fitbit's API
		'''
		oauth = OAuth2Session(self.clientID, redirect_uri=self.callback_URL, scope=self.scope)
		
		self.authorization_URL, self.state = oauth.authorization_url(self.authorization_URI)

		print('Please go to this URL and copy the redirected URL here:\n{}'.format(self.authorization_URL))
		
		self.authorization_code = input('Enter the URL: ')

		self.authorization_code = self.authorization_code[self.authorization_code.find("code=")+5:self.authorization_code.find("&state=")]

	def getTokens(self):
		'''
		Gets access and refresh tokens
		'''
		self.headers = {
		    "Authorization": "Basic {}".format(self.client_encode),
		    "Content-Type": "application/x-www-form-urlencoded",
		}

		self.data = {
		  "clientId": "{}".format(self.clientID),
		  "grant_type": "authorization_code",
		  "redirect_uri": "{}".format(self.callback_URL),
		  "code": self.authorization_code,
		}

		self.response = requests.post(self.token_request_URI , headers=self.headers, data=self.data)

	def saveTokens(self, filename="fitbit_access_tokens.json"):
		#Save tokens to JSON file
		self.filename = filename
		with open(self.filename, 'w') as outfile:
			json.dump(self.response.text, outfile, ensure_ascii=False)

	def refreshTokens(self, filename="fitbit_access_tokens.json"):
		'''
		Refreshes the access token using the refresh token
		'''
		with open(filename) as json_file:  
			self.token_dict = json.loads(json.load(json_file))

		self.access_token = self.token_dict['access_token']
		self.refresh_token = self.token_dict['refresh_token']

		self.headers_refresh = {
		    "Authorization": "Basic {}".format(self.client_encode),
		    "Content-Type": "application/x-www-form-urlencoded",
		}

		self.data_refresh = {
		  "refresh_token": self.refresh_token,
		  "grant_type": "refresh_token",
		  "expires_in": 28800, #default = 28800s = 8hrs
		}

		self.response_refresh = requests.post(self.token_request_URI , headers=self.headers_refresh, data=self.data_refresh)
		# print(self.response_refresh.text)

		self.access_token_new = json.loads(self.response_refresh.text)['access_token']
		self.refresh_token_new = json.loads(self.response_refresh.text)['refresh_token']

		#Save tokens to JSON file
		with open(filename, 'w') as outfile:
			json.dump(self.response_refresh.text, outfile, ensure_ascii=False)

	def seeTokens(self, filename="fitbit_access_tokens.json"):
		'''
		Show current token credentials
		'''
		with open(filename) as json_file:  
			self.token_dict = json.loads(json.load(json_file))

		print('Access Token: {}'.format(self.token_dict['access_token']))
		print('Refresh Token: {}'.format(self.token_dict['refresh_token']))
		print('UserID: {}'.format(self.token_dict['user_id']))
		print('Expiration Duration: {}'.format(self.token_dict['expires_in']))
		print('Token Type: {}'.format(self.token_dict['token_type']))
		print('Scope: {}'.format(self.token_dict['scope']))


My_App_Credentials = FitbitAuthorization(cred.clientID, cred.clientSecret, cred.callback_URL)
# My_App_Credentials.establishConnection()
# My_App_Credentials.getTokens()
# My_App_Credentials.saveTokens()
My_App_Credentials.refreshTokens()
My_App_Credentials.seeTokens()