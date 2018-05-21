import logging, gensim
from gensim import similarities, corpora, models
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, date
import dateparser


dictionary = corpora.Dictionary.load('data/data.dict')
corpus = corpora.MmCorpus('data/data.mm')
print ("Loaded dictionary and corpus")

model = models.Word2Vec(texts_train, size=200, window=10, min_count=1, workers=10)
model.train(texts_train, total_examples=len(texts_train), epochs=100)
model.save("models/model.w2v")
