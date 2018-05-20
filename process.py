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

# print (df.columns)
# print (df['jobpost'][0])
np.random.shuffle(df.values)
documents = df['jobdescription']
# documents = df['Title']
# titles = df['title']
# companies = list(df['company'].values)
with open("stopwords.txt", "r") as f:
    stoplist = f.readlines()
    for word in range(len(stoplist)):
        stoplist[word] = stoplist[word].replace("\n", "")

secondary_stoplist = "\\ / . -".split()
# stoplist = list(set('for a of the and to in at • is will on as our or we an work new with you are be · all other inc your about becasue that their this too each few during has by job - /'.split()))
texts = [[word for word in re.split(r'\s+|[,;.-]\s*', str(document).lower()) if word not in stoplist] for document in documents]

dictionary = corpora.Dictionary(texts)
dictionary.save('data.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('data.mm', corpus)
model = models.Word2Vec(texts, size=200, window=10, min_count=1, workers=10)
# model = models.Doc2Vec(texts, size=25, window=10, min_count=1, workers=10)
model.train(texts, total_examples=len(texts), epochs=100)
# print (model.wv['software'])
model.save("model.w2v")
# print (model.wv.most_similar(positive=['software']))
# print (model.wv.similarity('c++', 'java'))
# print (model.wv.similarity('business', 'java'))
# print (model.wv.doesnt_match("c++ java python finance".split()))
# print (model.wv.doesnt_match("business law python finance".split()))

# print (model.wv.syn0)
# red_factor = 0.005
# clusters = int(len(texts) * red_factor)
# print ("Clusters: %s" % clusters)
# mod = KMeans(n_clusters=clusters).fit(model.wv.syn0)
# mod = MeanShift(n_jobs=-1).fit(model.wv.syn0)
# # mod = GaussianMixture().fit(model.wv.syn0)
# print(mod.labels_)
# plt.scatter(model.wv.syn0[:,0],model.wv.syn0[:,1], c=mod.labels_, cmap='rainbow')
# plt.show()
#
# print (mod.predict([model.wv['c++']]))

# print (model.wmdistance("Software engineer", "programmer"))
# print (model.wmdistance("software developer", "mechanical engineer"))

model = models.TfidfModel(corpus, id2word=dictionary)
model.save("model.tfidf")

# m2 = similarities.MatrixSimilarity(model[corpus])
# m2.save("similarity.matrix")
