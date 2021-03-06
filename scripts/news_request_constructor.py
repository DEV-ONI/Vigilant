
import requests
import inspect
import json
import urllib
from pprint import pprint

from vigilant_custom_log import custom_log
from request_decoder import NewsAggregate as news_agg
from requests import exceptions as ex


class ArticlesFetched:

	def __init__(self, *contexts):

		self.news_token = 'ed35beacc77447db90a92ab1337e52c6'
		self.newsriver_token = 'sBBqsGXiYgF0Db5OV5tAw0VKhAq8zkkjCrqKwmR3QN_TyztikgQKHW6toOuSNN6Tn2pHZrSf1gT2PUujH1YaQA'
		self.news_keywords = ''
		self.newsriver_keywords = ''
		custom_log(contexts)

		for context in contexts:

			if self.news_keywords == '':
				operator = ''
				operator_2 = ''
			else:
				operator = '+'
				operator_2 = ' OR '

			self.news_keywords += operator + context
			rcontext = str('%22' + context + '%22') if ' ' in context else context
			self.newsriver_keywords += operator_2 + 'text:' + rcontext

	def news_api_request(
		self, searchBy = 'everything', sortBy='relevancy',
		pageSize = '', page = '', **extra_queries
	):

		request_url = 'https://newsapi.org/v2/'
		request_url += searchBy

		arg_spec = inspect.getfullargspec(self.news_api_request)

		payload = dict(
			(kwargs, vals) for kwargs, vals in zip(arg_spec.args[2:], arg_spec.defaults[2:]) if vals is not ''
		)

		# add keywords or phrases to the request
		payload['q'] = self.news_keywords
		headers = {}
		headers['X-Api-Key'] = self.news_token

		# log(self, payload)

		response = requests.get(url=request_url, headers=headers, params=payload)

		# log(self, response.json())
		loaded = json.loads(response.text)
		pprint(loaded)

	def news_river_api_request(
			self, bool_operator = 'OR', language = 'EN',
			sortBy='_score', sortOrder='DESC', limit=100
	):

		valid_operators = ['AND', 'OR', 'NOT']
		valid_country_codes = []
		request_url = 'https://api.newsriver.io/v2/search'
		response = None

		"""
		if bool_operator not in valid_operators:
			pass
			# raise some exception
		else:
			if bool_operator is not 'AND':
				self.newsriver_keywords.replace('AND',
					bool_operator.center(len(bool_operator)+2*len(' '), ' '))
 
		
		
		if countryCode not in valid_country_codes:
			pass
			# raise some exception
		else:
			if bool_operator is not 'AND':
				self.newsriver_keywords.replace('AND', bool_operator)

		"""

		payload = {}
		payload['query'] = self.newsriver_keywords + ' AND ' + 'language:{}'.format(language)

		arg_spec = inspect.getfullargspec(self.news_river_api_request)
		for kwargs, vals in zip(arg_spec.args[2:], arg_spec.defaults[1:]):
			payload[kwargs] = vals

		params = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)

		headers = {}
		headers["Authorization"] = self.newsriver_token

		response = requests.get(request_url, headers=headers, params=params)
		# response.raise_for_status()
		custom_log(response.request.body)

		"""
		try:
			response = requests.get(request_url, headers=headers, params=params, timeout = (15, 30))
			response.raise_for_status()
			custom_log(response)
		
		except ex.HTTPError:
			pass
			# handle exception
		except ex.Timeout:
			pass
			# handle exception
		"""
		custom_log(response.text)
		loaded = json.loads(response.text)
		na = news_agg(response)
		compiled = na.json_decodecompile()
		custom_log(compiled)


# if __name__ is "__main__":

# A = ArticlesFetched('China', 'Duterte')
# A.news_api_request(pageSize='100', page='1')
# A.news_river_api_request(bool_operator= 'AND')










