import pandas as pd
import numpy as np
import logging, gensim
from gensim import similarities, corpora, models
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans, MeanShift
import re
import requests
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

r = requests.get("http://18.220.46.51:3000/api/queries/GetAvailableJobs")
r = r.json()

def get_docs(r):
    documents = []
    for i in r:
        documents.append(i['description'])
    return documents

documents = get_docs(r)

with open("assets/stopwords.txt", "r") as f:
    stoplist = f.readlines()
    for word in range(len(stoplist)):
        stoplist[word] = stoplist[word].replace("\n", "")

secondary_stoplist = "\\ / . -".split()
texts_save = [[word for word in re.split(r'\s+|[,;.-/\\?.]\s*', str(doc).lower()) if word not in stoplist] for doc in documents]

dictionary = corpora.Dictionary(texts_save)
dictionary.save('data/data.dict')
corpus = [dictionary.doc2bow(text) for text in texts_save]
corpora.MmCorpus.serialize('data/data.mm', corpus)

model = models.TfidfModel(corpus, id2word=dictionary)
model.save("models/model.tfidf")
