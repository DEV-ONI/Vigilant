from vigilant_custom_log import custom_log

class NewsAggregate:

	def __init__(self, response):
		if response is None:
			# raise an exception
			pass

		self.rjson = response.json()
		custom_log(self.rjson)

	# def expose_keys(self):

	def json_decodecompile(self, relevant_keys = ['title', 'text', 'url', 'website']):

		compiled_news = []
		title_occurence = []

		for element, i in zip(self.rjson, range(len(self.rjson))):
			# compiled

			if element['title'][0] in title_occurence:
				pass
			else:
				compiled_values = [element[key] if key in element else '' for key in relevant_keys]
				compiled_news.append(element.fromkeys(relevant_keys, compiled_news))
				title_occurence.append(element['title'][0])

				# debug
				custom_log('COMPILED VALUES: {}'.format(compiled_values))
				custom_log('COMPILED NEWS: {}'.format(compiled_news))

				custom_log("FORMAT /n")
				for key in relevant_keys:

					custom_log("key: {}, value: {}".format(key, element[key] if key in element.keys() else ''))

				custom_log("END \n")

		return compiled_news


