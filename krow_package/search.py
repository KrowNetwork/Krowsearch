import warnings
warnings.filterwarnings("ignore")
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')

import couchdb
import logging
from gensim import similarities, corpora, models
import pandas as pd
import numpy as np
import argparse
from datetime import datetime, date
import dateparser
import sys, os
import json
import time
import asyncio
loop = asyncio.get_event_loop()


write_file = "results.json"

def parse_date(date):
    return dateparser.parse(date).date()

async def get_sentence_difference(sent_1, sent_2, model, vector_avg):
    sent_list_1 = str(sent_1.lower()).split()
    sent_list_2 = str(sent_2.lower()).split()
    s1_use = 0
    s2_use = 0

    sent_sum_1 = np.zeros(200)
    sent_sum_2 = np.zeros(200)

    for word in sent_list_1:
        try:
            # word = word.lower()
            sent_sum_1 = np.add(np.array(model.wv[word]), sent_sum_1)
            s1_use += 1
        except:
            pass

    for word in sent_list_2:
        try:
            # word = word.lower()
            sent_sum_2 = np.add(np.array(model.wv[word]), sent_sum_2)
            s2_use += 1

        except:
            pass

    x = np.absolute(np.subtract(sent_sum_1 / s1_use, sent_sum_2 / s2_use))
    vector_avg += sum(x)/len(x)
    return vector_avg

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

async def calc(i):
    count = 1
    vector_avg = i[1]
    if term != "":
        vector_avg = await get_sentence_difference(term, df['description'][i[0]], model, vector_avg)
        vector_avg = await get_sentence_difference(term, df['title'][i[0]], model, vector_avg)
        count += 2

    return vector_avg / count

async def iterate_data(data):
    for i in data:
        yield i
        # await asyncio.sleep(0.5)

async def search(term):
    if args.t:
        now = time.time()
    # now = time.time()
    # print (term)
    vec_bow = dictionary.doc2bow(term.lower().split())
    vec_lsi = lsi[vec_bow]

    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    top = sims[:10]
    vals = []
    today = date.today()
    if args.t:
        loop_now = time.time()
    async for i in iterate_data(top):
        # i = top[u]
        vals.append([await calc(i), i[0]])
    if args.t:
        loop_now = time.time() - loop_now
    # tasks = [calc(term, i, model) for i in top]
    # x = await asyncio.wait(tasks)
    # print (tasks)

    # vals = await asyncio.gather(*[calc(term, i, model) for i in top])


    # print ("Processed all entries")
    # vals = normalize_differences(vals)
    # print ("Normalized differences")
    sims = sorted(vals, key=lambda item: item[0])

    c = 0
    # data = dict()
    data = str(df["ID"][sims[0][1]]) + " "
    for i in range(1, len(sims)):
        data += str(df["ID"][sims[i][1]]) + " "
        # for i in db.view("_all_docs"):
        #     if ("c5b8f44a-d818-48c7-b301-805bae81007d" in i['id']):
        #         print (i)
        #         print (db.get(i['id']))
        # data["%s" % i] = df["ID"][sims[i][1]]
    # os.system('cls')
    # print (json.dumps(data))
    print (data)
    fin = time.time()
    if args.t:
        print ("Total Time: %s" % (fin - now))
        print ("Loop time: %s" % (loop_now))
    # print (time.time() - now)

    # os.remove(parse_file)
    sys.stdout.flush()


parser = argparse.ArgumentParser(description='search')
parser.add_argument('-t', action='store_true')
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
    # term = sys.stdin.readlines()
    # term = np.array(term)[0]

    term = input()
    # asyncio.ensure_future()
    loop.run_until_complete(search(term))
    # time.sleep(3)
    # os.system('cls')
    # with open(parse_file, "w") as f:
    #     f.write("succ")
