from vigilant_custom_log import log

class NewsAggregate:

	def __init__(self, response):
		if response is None:
			# raise an exception
			pass

		self.rjson = response.json()

	# def expose_keys(self):

	def json_decodecompile(self, relevant_keys = ['title', 'url', 'website']):

		compiled_news = {}

		for elements, i in zip(self.rjson, range(len(self.rjson))):
			compiled_news[i] = elements.fromkeys(relevant_keys)
			log(elements.fromkeys(relevant_keys))

		return compiled_news









