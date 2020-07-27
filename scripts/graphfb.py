
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from vigilant_custom_log import log
import mechanize
import time

class UrlRedirectedToken:

	def __init__(self, auth_url):
		self.auth_url = auth_url

	def __call__(self, driver):

		if self.auth_url != driver.current_url and 'access_token' in driver.current_url:
			q_start = driver.current_url.find('access_token')

			# code query string value terminates with '&' character
			q_end = driver.current_url.find('&') - 1
			return driver.current_url[q_start: q_end]

class UrlRedirected:

	def __init__(self, auth_url):
		self.auth_url = auth_url

	def __call__(self, driver):

		if self.auth_url != driver.current_url:
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
		'response_type': 'token', 'scope': 'manage_pages, publish_pages, publish_to_groups'}
	):

		response = requests.get(url=self.auth_url, params=payload)

		return response.url

	def mechanized_login(self, url = '', email = '', passw = ''):

		mech_br = mechanize.Browser()
		mech_br.set_handle_robots(False)
		mech_br.set_header('User-Agent',
			value='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36')

		cookies = mechanize.CookieJar()
		mech_br.set_cookiejar(cookies)
		mech_br.set_handle_equiv(True)
		mech_br.set_handle_gzip(True)
		mech_br.set_handle_redirect(True)
		mech_br.set_handle_referer(True)

		mech_br.open(url)

		for form in mech_br.forms():
			if form.attrs['id'] == 'login_form':
				mech_br.form = form
				break

		log(self, mech_br.form)

		mech_br.form.set_value(email, name='email')
		mech_br.form.set_value(passw, name='pass')
		response = mech_br.submit()

		# log(self, response.geturl())

		driver = webdriver.Chrome()
		driver.get(response.geturl())

	def automated_login(self, url = '', email = '', passw = ''):

		chrome_options = Options()
		# chrome_options.add_argument('--
		chrome_options.add_argument('--disable-notifications')
		chrome_options.add_argument('--start-maximized')
		driver = webdriver.Chrome(options=chrome_options)
		driver.get(url)

		#form fill with email and password


		email_element = driver.find_element(by='id', value='email')
		passw_element = driver.find_element(by='id', value='pass')
		loginform_element = driver.find_element(by='id', value='login_form')
		email_element.send_keys(email)
		passw_element.send_keys(passw)
		loginform_element.submit()


		wait = WebDriverWait(driver, 120)
		nextbtn_sel = '#platformDialogForm > div > div.clearfix._ikh > div > div > div > div._6lqs > div._6lqx > div._6-v1 > button:nth-child(2)'
		nextbtn_sel_2 = '#platformDialogForm > div > div.clearfix._ikh > div > div > div > div._6lqs > div._6lqx > div > div > button'
		nextbtn_sel_3 = '#platformDialogForm > div > div.clearfix._ikh > div > div > div > div._6lqs > div._6lqx > div > div > button'
		nextbtn_sel_4 = '#platformDialogForm > div > div.clearfix._ikh > div > div > div > div._6lqs > div._6lqx > div > button'
		# page_selector = '#js_th_112023553484105'
		page_sel = '#platformDialogForm > div > div.clearfix._ikh > div > div > div > div._6-wr > div > div:nth-child(2) > div._6-v_ > fieldset > label > span > span._puz > span > input'

		element_sequence = [nextbtn_sel, page_sel, nextbtn_sel_2, nextbtn_sel_3, nextbtn_sel_4]

		# self.click_element_sequence(driver, element_sequence)
		log(self, self.extract_access_token(driver))

		"""
		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, nextbutton_selector)))
		nextbutton_element = driver.find_element(by='css selector', value=nextbutton_selector)
		nextbutton_element.click()

		wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_25_i')))
		pageselect_element = driver.find_element(by='class name', value='_25_i')
		pageselect_element.click()

		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, nextbutton_selector_2)))
		nextbutton_element_2 = driver.find_element(by='css selector', value=nextbutton_selector_2)
		nextbutton_element_2.click()

		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, nextbutton_selector_3)))
		nextbutton_element_3 = driver.find_element(by='css selector', value=nextbutton_selector_3)
		nextbutton_element_3.click()

		wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, nextbutton_selector_4)))
		nextbutton_element_4 = driver.find_element(by='css selector', value=nextbutton_selector_4)
		nextbutton_element_4.click()
		"""

	def click_element_sequence(self, driver, element_sequence):

		wait = WebDriverWait(driver, 120)

		for css_selector in element_sequence:

			wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
			element_id = driver.find_element(by='css selector', value=css_selector)
			element_id.click()

	def extract_access_token(self, driver):
		try:
			wait = WebDriverWait(driver, 120)
			access_token = wait.until(UrlRedirectedToken(self.auth_url))
		finally:
			driver.close

		return access_token






auth_graph = AuthenticatedGraphRequest()
url = auth_graph.invoke_login_dialog()
auth_graph.automated_login(
	url=url,
	email='contact.2.mng@gmail.com',
	passw='_-_OnI77'
)



