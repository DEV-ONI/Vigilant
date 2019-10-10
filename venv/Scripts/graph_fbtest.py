import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from vigilant_custom_log import log
import mechanize
import time

class UrlRedirected:

	def __init__(self, auth_url):
		self.auth_url = auth_url

	def __call__(self, driver):

		if self.auth_url != driver.current_url and 'access_token' in driver.current_url:
			q_start = driver.current_url.find('access_token')

			# code query string value terminates with '&' character
			q_end = driver.current_url.find('&') - 1
			return driver.current_url[q_start: q_end]

class AuthenticatedGraphRequest:

	def __init__(
		self,
		auth_url = 'https://www.facebook.com/v4.0/dialog/oauth',
		redirect_uri = 'https://www.facebook.com/connect/login_success.html'
	):

		self.auth_url = auth_url
		self.redirect_uri = redirect_uri

	def invoke_login_dialog(
		self,
		payload={'client_id': '2352685261493756', 'client_secret': 'ebd80dc6573729ebc67eb6756ea129c3',
		'redirect_uri': 'https://www.facebook.com/connect/login_success.html', 'state': '{st=state123abc,ds=123456789}',
		'response_type': 'token', 'scope': 'manage_pages'}
	):

		response = requests.get(url=self.auth_url, params=payload)

		driver = webdriver.Chrome()
		driver.get(response.url)
		time.sleep(6000)

agr=AuthenticatedGraphRequest()
agr.invoke_login_dialog()