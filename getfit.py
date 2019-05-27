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

#Instantiate my user authorization to get access and refresh tokens
My_App = FitbitAuthorization(cred.clientID, cred.clientSecret, cred.callback_URL)

# My_App.establishConnection()
# My_App.getTokens()
# My_App.saveTokens()
# My_App.seeTokens()


# My_App.refreshTokens()

access_token = My_App.retrieveAccessToken()

My_User = UserData(access_token)
print(My_User.getBadges())



