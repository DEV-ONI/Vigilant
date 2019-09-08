import spacy
from spacy.language import Language
from spacy.pipeline import EntityRecognizer
from spacy.vocab import Vocab

import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords as sw
from glove_load import GloveVectors as gv
# from nltk.corpus import pun

import numpy as np

from vigilant_custom_log import custom_log

# from pprint.PrettyPrint import pprint

doc_string = """
Duterte said he fired Faeldon because he insisted at the Senate committee hearing that rape-slay convict and ex-Calauan Lagunar Mayor Antonio Sanchez was eligible for early release under the good conduct time allowance (GCTA) law.
"""

class NLPProcess():

	def __init__(self, doc_string='', doc_elements=''):
		"""
		initializes NLP process object, initializes spacy model and doc
		:param doc_string: string to be subjected to textual analysis (optional)
		:param doc_elements: element sit to be subjected to textual analysis
		"""
		self.doc_string = doc_string
		self.doc_elements = doc_elements
		self.nlp = Language(Vocab())
		self.nlp = spacy.load("en_core_web_sm")
		# self.nlp.vocab.vectors.from_glove("glove6B/glove.6B.50d.txt")
		self.document = self.nlp(self.doc_string)

	def spacy_ner_labelled(self):
		"""
		:return: returns a mapping type with named entity : entity category
		"""

		"""
		print('DOCUMENT ENTS: {}'.format(self.document.ents))
		text = [span.text for span in self.document.ents]
		label = [span.label_ for span in self.document.ents]
		ent_map = dict(set(zip(text, label)))
		print(ent_map)
		"""

		sentences = []
		print('DOCUMENT ENTS: {}'.format(self.document.ents))

		for sent in self.document.sents:

			temp = self.nlp(sent.text)
			text = [span.text for span in temp.ents]
			label = [span.label_ for span in temp.ents]
			sentence_ents = dict(set(zip(text, label)))
			sentences.append(sentence_ents)

		return sentences

	def spacy_ner(self):

		sentences = []

		for sent in self.document.sents:

			temp = self.nlp(sent.text)
			ents = [span.text for span in temp.ents]
			sentences.append(ents)


		return sentences

	def spacy_sim(self):
		pass

	def candidate_chunker(self):
		noun_chunks = []

		for chunk in self.document.noun_chunks:
			custom_log(chunk)
			noun_chunks.extend(
				[t.text for t in chunk
				 if t.text not in [ent.text for ent in chunk.ents]
				 if t.pos_ is 'NOUN' or t.pos_ is 'ADJ'
				]
			)

		custom_log(noun_chunks)

		return noun_chunks

	def get_tokenset(self, bool_lemma=True, nest=True):
		"""
		creates a token set for each sentence while removing punctuation marks and escape characters
		:param bool_lemma: if true, returns a set of lemma tokens. if false, returns tokens
		:param omit_ner: if true, omits named entities
		:return: returns set of tokens
		"""

		self.docset = []
		self.docset_lemma = []
		self.nes = set(span.text for span in self.document.ents)


		"""
		if bool_lemma is True:
			
			for sent in self.document.sents:

				self.docset_lemma.append(
					[token.lemma_ for token in sent
					 if not ('\u0000' <= token.text <= '\u002F'
							 or '\u003A' <= token.text <= '\u003E'
							 or '\u005B' <= token.text <= '\u005F'
							)
					 if not token in self.nes
					]
				)

			return self.docset_lemma
		
		else:

			for sent in self.document.sents:

				self.document_lemma.append(
					[token for token in sent
					 if not ('\u0000' <= token.text <= '\u002F'
							 or '\u003A' <= token.text <= '\u003E'
							 or '\u005B' <= token.text <= '\u005F'
							)
					 if not token in self.nes
					]
				)

			return self.docset
		"""

		self.doc_op = self.docset_lemma if bool_lemma else self.docset

		for sent in self.document.sents:

			sent_token = [token.lemma_.text if bool_lemma else token.text for token in sent
				if not ('\u0000' <= token.text <= '\u002F'
						 or '\u003A' <= token.text <= '\u003E'
						 or '\u005B' <= token.text <= '\u005F'
				)
				if not token in self.nes
			]
			self.doc_op.append(sent_token) if nest is True else self.doc_op.extend(sent_token)

		return self.doc_op

	def omit_stop(self, document):

		stopwords = sw.words('english')
		self.document_omitted = []

		for sentences in document:
			self.document_omitted.append(
				[token for token in sentences if token not in stopwords]
			)

		return self.document_omitted

	def omit_space(self, sent_set):

		singles_sets = []
		for sent in sent_set:
			single_set = []
			for _ in sent:
				# print(_)
				if ' ' in _:
					print(_)
					single_set.extend(_.split(' '))
				else:
					single_set.append(_)

			singles_sets.append(single_set)

		return singles_sets

	def set_difference(self, parent_set, child_set):

		diff_set = []

		for psets, csets in zip(parent_set, child_set):
			diff = set(psets).difference(set(csets))
			diff_set.append(diff)

		return diff_set



class NLPRelation():

	def __init__(self, token_set):
		self.token_set = token_set
		self.token_debug = 'rape'

	def semantic_cosine_similarity(self):
		pass

	def get_synset(self):
		syn = wn.synsets(self.token_debug, pos = wn.VERB)
		custom_log(syn)
		# instantiate a list of related words where the '_' char is replaced with a space
		syn_list = [l.name().replace('_', ' ') for s in syn for l in s.lemmas()]
		custom_log(syn_list)
		syn_set = set(syn_list)
		custom_log(syn_set)

class Vigilant:
	"""
	Vigilant class contains semantic analysis and comparison methods that attempt to find the closest semantically
	related sentences. Named entities, whether raw string or categorical names, are considered when parsing documents.
	"""
	def __init__(self):
		self.nlp = Language()
		self.nlp.from_disk(r'glove6B/glove-6B')
		self.nlpt = NLPProcess(doc_string=doc_string)

	def key_extractor(self):
		candidate_chunks = self.nlpt.candidate_chunker()
		candidate_score = {}
		token_set = self.nlpt.get_tokenset(bool_lemma=False, nest=False)
		# custom_log(token_set)
		# custom_log(candidate_chunks)

		to_zero = lambda i: (abs(i)+i) if i < 0 else i
		to_ceiling = lambda i: len(token_set) if i > len(token_set) else i

		for candidate in candidate_chunks:
			score = 0
			no_instances = 0
			# custom_log(candidate)
			for index in find_all(candidate, token_set):
				no_instances += 1
				for neighbor in range(to_zero(index-5), to_ceiling(index+5)):
					if token_set[neighbor] in candidate_chunks and neighbor is not index:
						score += 1
						custom_log(token_set[neighbor])

			custom_log(no_instances)

			candidate_score[candidate] = score

		custom_log(candidate_score)

			# candidate_score[str(candidate)] += 1



		# for chunk in noun_chunks

	def max_correlate(self):
		"""
		:param self: implicitly passed instance of the binding class
		:param token_set: a nested collection containing the tokens per each parsed line of the document
		:return:
		"""

		# debugtest: vectorloading

		"""
		custom_log(token_sets)
		nlp = Language()
		nlp.from_disk(r'glove6B/glove-6B')
		for sets in token_sets:
			for token in sets:
					custom_log(nlp(token).vector)
		"""
		
	def string_vectorize(self, doc_string):

		nes_set = self.nlpt.spacy_ner()
		token_set = self.nlpt.get_tokenset(bool_lemma=True, nest=False)
		omitted_set = self.nlpt.omit_stop(token_set)
		custom_log(omitted_set)
		nes_single_set = self.nlpt.omit_space(nes_set)
		custom_log(nes_single_set)
		diff_set = self.nlpt.set_difference(omitted_set, nes_single_set)
		custom_log(diff_set)

		document_vectorized = []
		for set in diff_set:
			searchable_words = len(set)
			sentence_vectorized = np.zeros((1, 50))
			for token in set:
				if not self.nlp(token).vector.any():
					searchable_words - 1
				else:
					sentence_vectorized += self.nlp(token).vector
			np.divide(sentence_vectorized, searchable_words)

			document_vectorized.append(sentence_vectorized)

		custom_log(document_vectorized)

"""

def find_all(element, list, index=0):
	index_list = []
	index = index
	try:
		index = list.index(element, index)
		# custom_log(index)
		index_list.append(index)
		if index != len(list)-1:
			find_all(element, list, index+1)
		else:
			return index_list
	except ValueError:
		return index_list
"""

def find_all(element, list):
	offset = 0
	index = 0

	while index != len(list):

		try:
			index = list.index(element, list.index(element) + offset)
			offset += 1
			yield index

		except ValueError:
			return


"""
nlpt = NLPProcess(doc_string=doc_string)
nes_set = nlpt.spacy_ner()
token_set = nlpt.get_tokenset(True)
omitted_set = nlpt.omit_stop(token_set)


print(token_set)
print(omitted_set)
print('NES_SET {} '.format(nes_set))

nes_set_single = nlpt.omit_stop(nes_set)

print(nes_set_single)

diff_set = nlpt.set_difference(omitted_set, nes_set_single)
"""

v = Vigilant()
# v.max_correlate()
# v.string_vectorize(doc_string)
v.key_extractor()


"""
nlpr = NLPRelation('')
nlpr.get_synset()
"""






