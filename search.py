import logging, gensim
from gensim import similarities, corpora, models
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, date
import dateparser

def parse_date(date):
    # return datetime.strptime(date, "%b %d, %Y").date()
    return dateparser.parse(date).date()

def get_sentence_difference(sent_1, sent_2, model):
    sent_list_1 = str(sent_1).split()
    sent_list_2 = str(sent_2).split()
    s1_use = 0
    s2_use = 0

    sent_sum_1 = np.zeros(50)
    sent_sum_2 = np.zeros(50)

    for word in sent_list_1:
        try:
            word = word.lower()
            sent_sum_1 = np.add(np.array(model.wv[word]), sent_sum_1)
            s1_use += 1
        except:
            pass

    for word in sent_list_2:
        try:
            word = word.lower()
            sent_sum_2 = np.add(np.array(model.wv[word]), sent_sum_2)
            s2_use += 1

        except:
            pass

    x =  np.absolute(np.subtract(sent_sum_1 / s1_use, sent_sum_2 / s2_use))
    return sum(x)/len(x)

def company_similarity_scorer(sent_1, sent_2):
    sent_1 = str(sent_1).lower()
    sent_2 = str(sent_2).lower()

    score = 0

    for word in sent_1.split():
        if word not in sent_2:
            score += 1.5

    return score

def normalize_differences(diffs):
    vals = [i[0] for i in diffs]
    max_diff = max(vals)
    min_diff = min(vals)
    normed = (vals - min_diff)/max_diff
    for i, a in zip(diffs, normed):
        i[0] = a
    return diffs



parser = argparse.ArgumentParser(description='search')
parser.add_argument('--title',
                    help='job title to search for', default="")
parser.add_argument('--company',
                    help='company to search for', default=None)
args = parser.parse_args()

df = pd.read_csv('data.csv')
# print (df['date'])
# exit()
# logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


dictionary = corpora.Dictionary.load('data.dict')
corpus = corpora.MmCorpus('data.mm')
print ("Loaded dictionary and corpus")

# lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=200)
# lsi = models.LdaModel(corpus, id2word=dictionary, num_topics=50, passes=5, eval_every=1)
# lsi = models.LdaSeqModel(corpus, id2word=dictionary, num_topics=100, eval_every=10 passes=100)
lsi = models.TfidfModel.load("model.tfidf")
print ("Loaded TFIDF model")

model = models.Word2Vec.load("model.w2v")
print ("Loaded Word2Vec")

# index = similarities.MatrixSimilarity.load("similarity.matrix")
index = similarities.MatrixSimilarity(lsi[corpus])
print ("Created similarity model")

term = args.title
vec_bow = dictionary.doc2bow(term.lower().split())
vec_lsi = lsi[vec_bow]

sims = index[vec_lsi]
sims = sorted(enumerate(sims), key=lambda item: -item[1])

top = sims#[:1000]
vals = []
today = date.today()
for i in top:
    count = 1
    vector_avg = i[1]
    # delta = today - parse_date(str(df['OpeningDate'][i[0]]))
    # vector_avg += delta.days / 365
    if args.title != "":
        vector_avg += get_sentence_difference(args.title, df['jobdescription'][i[0]], model)
        vector_avg += get_sentence_difference(args.title, df['jobtitle'][i[0]], model)
        count += 2
    if args.company != None:
        vector_avg += company_similarity_scorer(args.company, df['company'][i[0]])#get_sentence_similarity(df['Company'][i[0]], args.company, model)
        count += 1
    # vals.append([model.wmdistance(doc, text), i[0]])
    vals.append([vector_avg / count, i[0]])

print (vals)
print ("Processed all entries")
# normalize_differences(vals)
print ("Normalized differences")
sims = sorted(vals, key=lambda item: item[0])

c = 0
for i in sims[:10]:
    print ("Company: %s" % df['company'][i[1]])
    print ("Title: %s" % df['jobtitle'][i[1]])
    print ("Difference Score: %s" % sims[c][0])
    c += 1
    print ("")
    print ("")
