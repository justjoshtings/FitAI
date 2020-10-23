'''
I. Establish initial connection to gain access and refresh token from Fitbit API.
II. Various methods to interact with Fitbit's REST API.
'''

'''
Import tools
'''
import requests
from requests_oauthlib import OAuth2Session
import json
import credentials as cred
import base64
import pandas as pd
import simplejson as json
from HelperFunctions import HelperFunctions

class FitbitAuthorization:
	'''
	Object for initiating Fitbit OAuth 2.0, getting access tokens, saving, and refreshing tokens.

	Have methods:
		establishConnection(self) 
			- Establish OAuth 2.0 connection with Fitbit's API and get authorization code.

		getTokens(self) 
			- Exchange authorization code with Fitbit to get access and refresh tokens.

		saveTokens(self, filename="fitbit_access_tokens.json") 
			- Saves tokens to JSON file. Default filename specified.

		refreshTokens(self, filename="fitbit_access_tokens.json")
			- Refreshes the access token using the refresh token and saves back to JSON file.

		seeTokens(self, filename="fitbit_access_tokens.json")
			- Prints tokens information for display.

		retrieveAccessToken(self, filename="fitbit_access_tokens.json")
			- Returns the current access token.
	'''
	def __init__(self, clientID, clientSecret, callback_URL, default_filename="fitbit_access_tokens.json"):
		self.clientID = clientID 
		self.clientSecret = clientSecret
		self.callback_URL = callback_URL
		self.authorization_URI = 'https://www.fitbit.com/oauth2/authorize'
		self.token_request_URI = 'https://api.fitbit.com/oauth2/token'
		self.client_encode = base64.b64encode((self.clientID+':'+self.clientSecret).encode()).decode('utf-8')
		self.filename = default_filename
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
	    
		self.hfn = HelperFunctions()

	def establishConnection(self):
		'''
		Establish OAuth 2.0 connection with Fitbit's API
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

		try:
			self.response = requests.post(self.token_request_URI , headers=self.headers, data=self.data)
			self.response.raise_for_status()
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

	def saveTokens(self):
		'''
		Save tokens to JSON file
		'''
		with open(self.filename, 'w') as outfile:
			json.dump(self.response.text, outfile, ensure_ascii=False)

	def refreshTokens(self):
		'''
		Refreshes the access token using the refresh token
		'''
		with open(self.filename) as json_file:  
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

		try:
			self.response_refresh = requests.post(self.token_request_URI , headers=self.headers_refresh, data=self.data_refresh)
			self.response_refresh.raise_for_status()
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

		self.access_token_new = json.loads(self.response_refresh.text)['access_token']
		self.refresh_token_new = json.loads(self.response_refresh.text)['refresh_token']

		#Save tokens to JSON file
		with open(self.filename, 'w') as outfile:
			json.dump(self.response_refresh.text, outfile, ensure_ascii=False)

	def seeTokens(self):
		'''
		Show current token credentials
		'''
		with open(self.filename) as json_file:  
			self.token_dict = json.loads(json.load(json_file))

		print('Access Token: {}'.format(self.token_dict['access_token']))
		print('Refresh Token: {}'.format(self.token_dict['refresh_token']))
		print('UserID: {}'.format(self.token_dict['user_id']))
		print('Expiration Duration: {}'.format(self.token_dict['expires_in']))
		print('Token Type: {}'.format(self.token_dict['token_type']))
		print('Scope: {}'.format(self.token_dict['scope']))

	def retrieveAccessToken(self):
		'''
		Returns current access token
		'''
		with open(self.filename) as json_file:
			self.token_dict = json.loads(json.load(json_file))

		return self.token_dict['access_token']

	def testConnection(self):
		'''
		Tests connection for token expiry
		'''
		self.access_token = self.retrieveAccessToken()

		self.secret_header = {'Authorization': 'Bearer {}'.format(self.access_token)}

		try:
			self.r = requests.get('https://api.fitbit.com/1/user/-/badges.json', headers=self.secret_header, timeout=10)
			self.r.raise_for_status()
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
			self.refreshTokens()
			self.r = requests.get('https://api.fitbit.com/1/user/-/badges.json', headers=self.secret_header, timeout=10)
			self.r.raise_for_status()
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)


class FitbitAPI:
	'''
	Object to setup the foundation and metadata needed to return based on an input category and endpoint.
	Parent class to Endpoints class.
	'''
	def __init__(self, access_token):
		self.access_token = access_token
		self.secret_header = {'Authorization': 'Bearer {}'.format(self.access_token)}

		self.baseAPI = 'https://api.fitbit.com'

		'''
		1. Need to map the rest of the API end points to this dict.
		2. For the {resource-path} KeyErrors here and others where inputs are needed, need to figure out what inputs it needs and how to get the inputs in
			-- smaller dicts for resource path options?
		'''
		
		self.API_endpoints_dict = {

				'User': {
						'Badges': '/1/user/-/badges.json',
						'Profile': '/1/user/-/profile.json',
						},
				'Sleep':{
						'Sleep Logs by Date': '/1.2/user/{}/sleep/date/{}/{}.json' #user-id = '-', startdate, enddate
						}
		}

		self.hfn = HelperFunctions()

		self.sleep_days_threshold = 100

	def makeAPICall(self, endpoint):
		'''
		Make API call
		'''
		self.API_endpoint = endpoint

		try:
			self.r = requests.get(self.API_endpoint, headers=self.secret_header, timeout=10)
			self.r.raise_for_status()
		except requests.exceptions.HTTPError as errh:
			print ("Http Error:",errh)
		except requests.exceptions.ConnectionError as errc:
			print ("Error Connecting:",errc)
		except requests.exceptions.Timeout as errt:
			print ("Timeout Error:",errt)
		except requests.exceptions.RequestException as err:
			print ("OOps: Something Else",err)

		# print(self.r.status_code)
		# print(self.r.text)

		try:
			return self.r.text
		except AttributeError as atterr:
			print('Connection did not go through, try again!')

	def getGenericEndpoint(self, category, subcategory):
		'''
		Make API GET call based on parameters created on object EndPoints instantiation and returns the JSON output.
		This is a generic endpoint where only the category and subcategory are needed:
			- User, Badges
			- User, Profile
		'''
		self.endpoint = self.baseAPI+self.API_endpoints_dict[category][subcategory]
		self.data_out = self.makeAPICall(self.endpoint)
		return self.data_out

	
	def getSleepEndpoint(self, category, subcategory, startdate, enddate):
		'''
		Make API GET call based on parameters created on object EndPoints instantiation and returns the JSON output.

		Max date range possible to download is 100 days
		'''
		start_dates, end_dates = self.hfn.dates_between(startdate, enddate, self.sleep_days_threshold)

		self.df_out = pd.DataFrame()
		
		for i in range(0,len(start_dates)):
			self.endpoint = self.baseAPI+self.API_endpoints_dict[category][subcategory].format('-', start_dates[i], end_dates[i])
			self.json_data_out = json.loads(self.makeAPICall(self.endpoint))

			# Flatten the JSON to a PD DF
			self.df = pd.io.json.json_normalize(self.json_data_out ['sleep'])

			self.df_out = self.df_out.append(self.df)

		# Save to Excel
		self.hfn.df_to_excel(self.df_out, 'FitBit_API_Data', 'SleepLog')
		# Store in DB: sleep table
		print(self.df_out.head(5))
		# self.hfn.df_to_db(self.df_out)

		return self.df_out
	








# api_endpoints = {'Daily_Activity': '/1/user/-/activities/heart/date/{}/1d/1min.json', }

# secret_header = {'Authorization': 'Bearer {}'.format(secret_token)}

# today_date = dt.today().strftime('%Y-%m-%d')

# query_str = API_base + api_endpoints['Daily_Activity'].format(today_date)
