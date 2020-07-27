# coding: utf8

import numpy as np

import spacy
from spacy.language import Language
from spacy.pipeline import EntityRecognizer
from spacy.vocab import Vocab

from vigilant_custom_log import custom_log

class GloveVectors:

	def __init__(self, dimensions):

		"""
		initializes the glove vector
		:param dimensions: dimenions of the word vector, specifies which glove text file to open
		"""

		valid_dim = [50, 100, 200, 300]
		if dimensions in valid_dim:
			pass
		else:
			# raise some exception if dimensions param is not in valid_dim
			# return none type
			pass

		self.glovedir = r'glove6B/glove.6B.{}d.txt'.format(str(dimensions))

	def load_model(self):
		"""
		loading glove vectors from directory into dictionary. use this method for manipulation outside
		nlp modules lacking vector loading methods
		:return: returns word vectors as a mapped type
		"""
		custom_log('LOADING GLOVE MODEL')
		glovefile = open(self.glovedir, 'r', encoding="utf8")

		# parses glove text
		for line in glovefile:
			splitLine = line.split()
			word = splitLine[0]
			embedding = np.array([float(val) for val in splitLine[1:]])
			model[word] = embedding
		custom_log('DONE')
		return model

	def load_tospacy(self, lang='en'):

		"""
		loads glove vectors from file specified in intialization, set vectors and save to disk
		:param lang:
		:return:
		"""

		if lang is None:
			# create blank multilanguage class with 'xx' if lang is None
			nlp = Language('xx')

		else:
			nlp = spacy.blank(lang)

		custom_log('PARSING GLOVE MODEL')

		with open(self.glovedir, 'r', encoding="utf8") as glove_file:
			model = {}
			for line in glove_file:
				split_line = line.split()
				word = split_line[0]
				embedding = np.array([float(val) for val in split_line[1:]])
				nlp.vocab.set_vector(word, embedding)

		custom_log('VECTORS SET, SAVING TO DISK')

		nlp.to_disk(r'glove6B/glove-6B')


def debug_test():
	"""
	debug test for vector loading and viewing from disk
	:return:
	"""

	gv = GloveVectors(50)

	nlp = Language()
	nlp.from_disk(r'glove6B/glove-6B')
	custom_log(nlp)
	word1 = nlp('president')
	word2 = nlp('leader')
	word3 = nlp('Trump')

	custom_log(word1.vector)
	custom_log(word2.vector)
	custom_log(word3.vector)

	custom_log(word1.similarity(word2))
	custom_log(word1.similarity(word3))

def numpy_test():

	custom_log(np.zeros((1, 30)))

# debug_test()
# numpy_test()