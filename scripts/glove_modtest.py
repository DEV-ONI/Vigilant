
# -*- coding: utf-8 -*-

import os
cwd = os.getcwd()
print(cwd)


gloveFile = 'glove6B/glove.6B.50d.txt'

import numpy as np

def load_glovemodel(gloveFile):
    print("Loading Glove Model")
    f = open(gloveFile,'r', encoding="utf8")
    model = {}
    for line in f:
        splitLine = line.split()
        word = splitLine[0]
        embedding = np.array([float(val) for val in splitLine[1:]])
        model[word] = embedding
    print("Done.",len(model)," words loaded!")
    return model

loaded_model = load_glovemodel(gloveFile)

print(loaded_model['president'])
print(loaded_model['bad thing'])
# print(loaded_model['Trump'])