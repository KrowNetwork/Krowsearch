import pandas as pd
import numpy as np
import logging, gensim
from gensim import similarities, corpora, models
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans, MeanShift
import re
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

df = pd.read_csv('data.csv')
df.drop_duplicates()
df.reset_index(drop=True)

df2 = pd.read_csv('data2.csv')
df2.drop_duplicates()
df2.reset_index(drop=True)

np.random.shuffle(df.values)
np.random.shuffle(df2.values)
documents = df['jobdescription']
doc2 = df2['description']

with open("stopwords.txt", "r") as f:
    stoplist = f.readlines()
    for word in range(len(stoplist)):
        stoplist[word] = stoplist[word].replace("\n", "")

secondary_stoplist = "\\ / . -".split()
texts_train = [[word for word in re.split(r'\s+|[,;.-/\\?.]\s*', str(document).lower()) if word not in stoplist] for document in documents]
texts_save = [[word for word in re.split(r'\s+|[,;.-/\\?.]\s*', str(doc).lower()) if word not in stoplist] for doc in doc2]

dictionary = corpora.Dictionary(texts_save)
dictionary.save('data.dict')
corpus = [dictionary.doc2bow(text) for text in texts_save]
corpora.MmCorpus.serialize('data.mm', corpus)

model = models.TfidfModel(corpus, id2word=dictionary)
model.save("model.tfidf")
