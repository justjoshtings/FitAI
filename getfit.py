'''
Import tools
'''
import requests
from requests_oauthlib import OAuth2Session
import numpy as np
import pandas as pd
from datetime import datetime as  dt
import json
from GetFitbitAPI import *
import credentials as cred
# from AnalyticsWorkBench import *

#1. Instantiate my user authorization to get access and refresh tokens
My_App = FitbitAuthorization(cred.clientID, cred.clientSecret, cred.callback_URL)

#2. Initial establish connection and get/save tokens. Only needed if invoking first access token.
# My_App.establishConnection()
# My_App.getTokens()
# My_App.saveTokens()

#3. Each connection, we retest connection and retrieve the current or refreshed access token.
My_App.testConnection() #Test connection and refresh token
access_token = My_App.retrieveAccessToken() #Retrieve access token

#4. Create My_Account connection object and get desired endpoints
My_Account = FitbitAPI(access_token) #Create my account object
sleep_logs = My_Account.getSleepEndpoint('Sleep', 'Sleep Logs by Date', '2019-05-01', '2020-10-21')

# print(sleep_logs)





