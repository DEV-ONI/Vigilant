*Would be happy to discuss this implementation in through email or in person*

Python, gloVe, Natural Language Processing
numpy, spacy, ntlk, wordnet, json, requests, urllib, inspect, logging

# Vigilant - Unsupervised Unique Keyphrase Extraction for Retrieval of Semantically Similar Articles 
### (Base objectives met) (Work in Progress) (Requires Debugging) (Requires Documentation) 

(see Vigilant.key_extractor in ne_classifier.py)
Parses a document string for tokens of noun phrases that correspond to the tags 'ADJ' and 'NOUN'. Each of these tokens become
candidate keys for evaluation. Each candidate key is compared against adjacent tokens within a specified window. The candidate keys are given a score based on their
semantic similarity to their neighbors based on the cosine similarity of their gloVe vector representation. Alpha and beta are reward coefficients for the 
number of instances of said candidate in the token set and their semantic similarity scores respectively. 

(see news_request_constructor.py)
Using these keyphrases, I can retrieve relevant articles by constructing an HTTP request with the keywords as payload to newsriver API
and parse these articles for semantically similar sentences.

[gloVe] (https://nlp.stanford.edu/projects/glove/)

[Unsupervised Key-phrase Extraction Algorithm which I implemented and modified] (https://pdfs.semanticscholar.org/cd96/3a530f1178833dc14f1d23545aaaacbf693e.pdf?fbclid=IwAR15EY2zMjX4YJq52H5KVS3T3U7fQUPAr-S1JbMNAgs1dJUZwmHgEroz-cY)

### Example:


"""
MANILA - Twenty-six years since Allan Gomez was murdered by former Calauan, Laguna Mayor Antonio Sanchez, the student's family still keeps his memorabilia.

Gomez was kidnapped by Sanchez's 6 aides on June 28, 1993, along with fellow University of the Philippines Los Baños student, 19-year-old Eileen Sarmenta, who was raped by the former mayor before being shot in the face, according to court records.

Sarmenta was presented to Sanchez as a "gift," while his aides beat up Gomez who was later shot dead as well.
"""


{'years': 0.3, 'former': 0.39, 'student': 1.1513, 'family': 1.4114, 'memorabilia': 0.8899, 'aides': 0.9704, 'fellow': 0.3, '19-year': -0.0649, 'old': -0.1783, 'mayor': 0.09, 'face': 0.698, 'court': 0.7834, 'records': 1.5971, 'gift': 0.6704}


The highest scoring keys are: records, family, and student.

1. University of the Philippines Los Baños student
2. court records
3. the student's family

