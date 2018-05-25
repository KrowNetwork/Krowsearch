import logging, gensim
from gensim import similarities, corpora, models
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, date
import dateparser
import re

df = pd.read_csv('datasets/data.csv')
df.drop_duplicates()
df.reset_index(drop=True)

np.random.shuffle(df.values)
documents = df['jobdescription']

with open("assets/stopwords.txt", "r") as f:
    stoplist = f.readlines()
    for word in range(len(stoplist)):
        stoplist[word] = stoplist[word].replace("\n", "")

secondary_stoplist = "\\ / . -".split()
texts_train = [[word for word in re.split(r'\s+|[,;.-/\\?.]\s*', str(document).lower()) if word not in stoplist] for document in documents]

dictionary = corpora.Dictionary.load('data/data.dict')
corpus = corpora.MmCorpus('data/data.mm')
print ("Loaded dictionary and corpus")

model = models.Word2Vec(texts_train, size=200, window=10, min_count=1, workers=10)
model.train(texts_train, total_examples=len(texts_train), epochs=100)
model.save("models/model.w2v")
