
import requests
import inspect
# import logging
import json
import urllib
from pprint import pprint

from vigilant_custom_log import log
from request_decoder import NewsAggregate as news_agg
import graphfb
# import

# logging.getLogger("parent")


class ArticlesFetched:

	def __init__(self, *contexts):

		self.news_token = 'ed35beacc77447db90a92ab1337e52c6'
		self.newsriver_token = 'sBBqsGXiYgF0Db5OV5tAw0VKhAq8zkkjCrqKwmR3QN_TyztikgQKHW6toOuSNN6Tn2pHZrSf1gT2PUujH1YaQA'
		self.news_keywords = ''
		self.newsriver_keywords = ''

		for context in contexts:

			if self.news_keywords == '':
				operator = ''
				operator_2 = ''
			else:
				operator = '+'
				operator_2 = ' AND '

			self.news_keywords += operator + context

			self.newsriver_keywords += operator_2 + 'text:' + context

	def news_api_request(self, searchBy = 'everything', sortBy='relevancy',
		pageSize = '', page = '', **extra_queries):

		request_url = 'https://newsapi.org/v2/'
		request_url += searchBy

		arg_spec = inspect.getfullargspec(self.news_api_request)

		payload = dict(
			(kwargs, vals) for kwargs, vals in zip(arg_spec.args[2:], arg_spec.defaults[2:]) if vals is not ''
		)

		# add keywords or phrases to the request
		payload['q'] = self.news_keywords
		# payload = arg_spec.annotations

		headers = {}
		headers['X-Api-Key'] = self.news_token

		log(self, payload)

		response = requests.get(url=request_url, headers=headers, params=payload)

		log(self, response.json())
		loaded = json.loads(response.text)
		pprint(loaded)

	def news_river_api_request(self, bool_operator = 'AND',
			sortBy='_score', sortOrder='DESC', limit=100):

		valid_operators = ['AND', 'OR', 'NOT']
		valid_country_codes = []
		request_url = 'https://api.newsriver.io/v2/search'

		if bool_operator not in valid_operators:
			pass
			# raise some exception
		else:
			if bool_operator is not 'AND':
				self.newsriver_keywords.replace('AND',
					bool_operator.center(len(bool_operator)+2*len('%20'), '%20'))

		"""
		
		if countryCode not in valid_country_codes:
			pass
			# raise some exception
		else:
			if bool_operator is not 'AND':
				self.newsriver_keywords.replace('AND', bool_operator)

		"""

		payload = {}
		payload['query'] = self.newsriver_keywords

		arg_spec = inspect.getfullargspec(self.news_river_api_request)
		for kwargs, vals in zip(arg_spec.args[2:], arg_spec.defaults[1:]):
			payload[kwargs] = vals

		params = urllib.parse.urlencode(payload, quote_via=urllib.parse.quote)

		headers = {}
		headers["Authorization"] = self.newsriver_token

		response = requests.get(request_url, headers=headers, params=params)
		loaded = json.loads(response.text)
		log(self, response.url)
		log(self, response.headers)
		# pprint(response.text)
		# jsonFile = response.json()

		na = news_agg(response)

		log(self, na.json_decodecompile())



# if __name__ is "__main__":

A = ArticlesFetched('China', 'Philippines')
# A.news_api_request()
A.news_river_api_request(bool_operator= 'AND')









