import logging, gensim
from gensim import similarities, corpora, models
import pandas as pd
import numpy as np
df = pd.read_csv('data job posts.csv')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary.load('data.dict')
corpus = corpora.MmCorpus('data.mm') # comes from the first tutorial, "From strings to vectors"
# print(corpus)

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=200)
# lsi = models.LdaModel(corpus, id2word=dictionary, num_topics=50, passes=5, eval_every=1)
# lsi = models.LdaSeqModel(corpus, id2word=dictionary, num_topics=100, eval_every=10 passes=100)

# lsi = models.TfidfModel(corpus, id2word=dictionary)#, num_topics=120)
print ()
# lsi.print_topics()
# # exit()
print ()
doc = "software developer"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]

index = similarities.MatrixSimilarity(lsi[corpus])

sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print (sims)


print (sims[:10])
for i in sims[:10]:
    print (df.ix[i[0]])
    print ("")

print (df['jobpost'][14])
