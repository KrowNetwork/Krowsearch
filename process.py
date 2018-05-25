import pandas as pd
import numpy as np
import logging, gensim
from gensim import similarities, corpora, models
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans, MeanShift
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

df = pd.read_csv('datasets/data2.csv')
df.drop_duplicates()
df.reset_index(drop=True)

np.random.shuffle(df.values)
documents = df['description']

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
