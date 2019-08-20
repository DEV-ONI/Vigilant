
"""
import facebook
import rauth
import json
from vigilant_custom_log import log

from rauth import OAuth2Service


vigilant_page = OAuth2Service(
		client_id='2352685261493756',
		client_secret='ebd80dc6573729ebc67eb6756ea129c3',
		base_url='https://www.facebook.com/v4.0/dialog/oauth'
)

redirect_uri = 'https://www.facebook.com/connect/login_success.html'
params = {'scope': 'manage_pages',
          'response_type': 'token',
          'redirect_uri': redirect_uri}



auth_url = vigilant_page.get_access_token(**params)
# auth_token = vigilant_page.get_auth_session(data=data, decoder=json.loads)
"""

import requests
from selenium import webdriver
import time
url = 'https://www.facebook.com/v4.0/dialog/oauth'
uri = 'https://www.facebook.com/connect/login_success.html'

payload = {'client_id': '2352685261493756', 'client_secret': 'ebd80dc6573729ebc67eb6756ea129c3', 'redirect_uri': uri, 'state': '{st=state123abc,ds=123456789}',
		   'response_type': 'token', 'scope': 'manage_pages'}

response = requests.get(url=url, params=payload)
print(response)
driver = webdriver.Chrome()
driver.get(response.url)
print(driver.current_url)



