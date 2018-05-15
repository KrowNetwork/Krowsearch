import logging, gensim
from gensim import similarities, corpora, models
import pandas as pd
import numpy as np
df = pd.read_csv('data job posts.csv')
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

dictionary = corpora.Dictionary.load('data.dict')
corpus = corpora.MmCorpus('data.mm') # comes from the first tutorial, "From strings to vectors"
# print(corpus)

# lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=200)
# lsi = models.LdaModel(corpus, id2word=dictionary, num_topics=50, passes=5, eval_every=1)
# lsi = models.LdaSeqModel(corpus, id2word=dictionary, num_topics=100, eval_every=10 passes=100)

lsi = models.TfidfModel(corpus, id2word=dictionary)#, num_topics=120)
print ()
# lsi.print_topics()
# # exit()

def get_sentence_similarity(sent_1, sent_2, model):
    sent_list_1 = sent_1.split()
    sent_list_2 = sent_2.split()
    s1_use = 0
    s2_use = 0

    sent_sum_1 = np.zeros(10)
    sent_sum_2 = np.zeros(10)

    for word in sent_list_1:
        try:
            word = word.lower()
            sent_sum_1 = np.add(np.array(model.wv[word]), sent_sum_1)
            s1_use += 1
        except:
            pass
        #     print ("err")

    for word in sent_list_2:
        try:
            word = word.lower()
            sent_sum_2 = np.add(np.array(model.wv[word]), sent_sum_2)
            s2_use += 1

        except:
            pass


    x =  np.absolute(np.subtract(sent_sum_1 / s1_use, sent_sum_2 / s2_use))
    print (x)
    return sum(x)/len(x)

print ()
doc = "financial analyst"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow]

index = similarities.MatrixSimilarity(lsi[corpus])

sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])
# print (sims)
model = models.Word2Vec.load("model.w2v")
top = sims[:10]
vals = []
for i in top:
    # print (i[0])
    full = df['jobpost'][i[0]]
    title = df['Title'][i[0]]
    # print (text)
    # print (get_sentence_similarity(text, doc, model))
    # exit()
    # vals.append([model.wmdistance(doc, text), i[0]])
    # print (text)
    vals.append([(get_sentence_similarity(full, doc, model) + get_sentence_similarity(title, doc, model)) / 2, i[0]])

sims = sorted(vals, key=lambda item: item[0])

print (sims[:10])
c = 0
for i in sims[:10]:
    print (df.ix[i[1]])
    print ("WMD: %s" % sims[c][0])
    c += 1
    print ("")
    print ("")

print (df['jobpost'][14])
