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

np.random.shuffle(df.values)
documents = df['jobdescription']

with open("stopwords.txt", "r") as f:
    stoplist = f.readlines()
    for word in range(len(stoplist)):
        stoplist[word] = stoplist[word].replace("\n", "")

secondary_stoplist = "\\ / . -".split()
texts = [[word for word in re.split(r'\s+|[,;.-/\\?.]\s*', str(document).lower()) if word not in stoplist] for document in documents]

dictionary = corpora.Dictionary(texts)
dictionary.save('data.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('data.mm', corpus)

model = models.Word2Vec(texts, size=200, window=10, min_count=1, workers=10)
model.train(texts, total_examples=len(texts), epochs=100)
model.save("model.w2v")

model = models.TfidfModel(corpus, id2word=dictionary)
model.save("model.tfidf")
