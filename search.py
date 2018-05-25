import logging, gensim
from gensim import similarities, corpora, models
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, date
import dateparser
import sys, os
import json

write_file = "results.json"
# print ("Yuh")
# sys.stdout.flush()
# exit()
# with open(parse_file, "w") as f:
#     f.write("succ")
def parse_date(date):
    return dateparser.parse(date).date()

def get_sentence_difference(sent_1, sent_2, model):
    sent_list_1 = str(sent_1).split()
    sent_list_2 = str(sent_2).split()
    s1_use = 0
    s2_use = 0

    sent_sum_1 = np.zeros(200)
    sent_sum_2 = np.zeros(200)

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
    new = []
    for i, a in zip(diffs, vals):
        new.append([(a - min_diff) / (max_diff - min_diff), i[1]])

    return new



parser = argparse.ArgumentParser(description='search')
parser.add_argument('--title',
                    help='job title to search for', default="")
parser.add_argument('--company',
                    help='company to search for', default=None)
args = parser.parse_args()

df = pd.read_csv('datasets/data2.csv')

dictionary = corpora.Dictionary.load('data/data.dict')
corpus = corpora.MmCorpus('data/data.mm')
# print ("Loaded dictionary and corpus")

lsi = models.TfidfModel.load("models/model.tfidf")
# print ("Loaded TFIDF model")

model = models.Word2Vec.load("models/model.w2v")
# print ("Loaded Word2Vec")

index = similarities.MatrixSimilarity(lsi[corpus])
# print ("Created similarity model")
while True:
    # term = json.loads(sys.stdin.readlines()[0])
    # while True:
    #     try:
    #         with open(parse_file, "r") as f:
    #             term = f.read()
    #             break
    #     except:
    #         pass
    term = sys.stdin.readlines()
    term = np.array(term)[0]
    # print (term)
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
        if term != "":
            vector_avg += get_sentence_difference(term, df['description'][i[0]], model)
            vector_avg += get_sentence_difference(term, df['title'][i[0]], model)
            count += 2
        if args.company != None:
            vector_avg += company_similarity_scorer(args.company, df['company'][i[0]])
            count += 1
        vals.append([vector_avg / count, i[0]])

    # print ("Processed all entries")
    vals = normalize_differences(vals)
    # print ("Normalized differences")
    sims = sorted(vals, key=lambda item: item[0])

    c = 0
    data = {}
    for i in sims:
        # print ("Company: %s" % df['company'][i[1]])
        # print ("Title: %s" % df['title'][i[1]])
        # print ("ID: %s" % df['ID'][i[1]])
        # print ("Difference Score: %s" % sims[c][0])
        # c += 1
        # print ("")
        # print ("")

        data["%s" % c] = df["ID"][i[1]]
        c += 1

    # print (json.dumps(data))
    print (data)

    # os.remove(parse_file)
    sys.stdout.flush()
    # with open(parse_file, "w") as f:
    #     f.write("succ")
