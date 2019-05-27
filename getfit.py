'''
Import tools
'''
import requests
from requests_oauthlib import OAuth2Session
import numpy as np
import pandas as pd
from datetime import datetime as  dt
import json

'''
Build API Endpoints
'''

API_base = 'https://api.fitbit.com'

api_endpoints = {'Daily_Activity': '/1/user/-/activities/heart/date/{}/1d/1min.json', }

secret_header = {'Authorization': 'Bearer {}'.format(secret_token)}

today_date = dt.today().strftime('%Y-%m-%d')

query_str = API_base + api_endpoints['Daily_Activity'].format(today_date)

'''
Make connection
'''
# r = requests.get(query_str, headers=secret_header)
# print(r.status_code)
# print(r.text)

