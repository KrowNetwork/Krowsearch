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
from dateutil.parser import parse
import dateparser
import sys, os
import json
import time
import asyncio
loop = asyncio.get_event_loop()
import requests
import operator
import geopy
from geopy import Nominatim
import re

geolocator = Nominatim()


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
            sent_sum_1 = np.add(np.array(model.wv[word]), sent_sum_1)
            s1_use += 1
        except:
            pass

    for word in sent_list_2:
        try:
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

def sort_ascending(array):
    for a in range(len(array)):
        i = array[a]
        array[a] = (i[0], i[1], r[i[0]]["created"])
    array = sorted(array, key=lambda item: item[2])
    array = [x[:2] for x in array]
    array = [x[::-1] for x in array]
    # print (array[0])
    return array

def sort_descending(array):
    for a in range(len(array)):
        i = array[a]
        array[a] = (i[0], i[1], r[i[0]]["created"])
    array = sorted(array, key=lambda item: item[2])[::-1]
    array = [x[:2] for x in array]
    array = [x[::-1] for x in array]
    return array

async def calc(i):
    count = 1
    vector_avg = i[1]
    if term != "":
        vector_avg = await get_sentence_difference(term, r[i[0]]['description'], model, vector_avg)
        vector_avg = await get_sentence_difference(term, r[i[0]]['title'], model, vector_avg)
        count += 2

    return vector_avg / count

async def iterate_data(data):
    for i in data:
        yield i

async def relevance_sort(top):
    vals = []
    async for i in iterate_data(top):
        vals.append([await calc(i), i[0]])
    
    return vals

async def search(term, location, sort_type):
    if args.t:
        now = time.time()
   
    vec_bow = dictionary.doc2bow(term.lower().split())
    vec_lsi = lsi[vec_bow]

    sims = index[vec_lsi]
    sims = sorted(enumerate(sims), key=lambda item: -item[1])

    top = sims[:10000]
    vals = []
    
    if sort_type == "ascending":
        # print ("sorting")
        sims = sort_ascending(top)
        sims = sims[:100]
    elif sort_type == "descending":
        sims = sort_descending(top)
        sims = sims[:100]

    else:
        if args.t:
            loop_now = time.time()
        async for i in iterate_data(top[:1000]):
            vals.append([await calc(i), i[0]])
        if args.t:
            loop_now = time.time() - loop_now
        sims = sorted(vals, key=lambda item: item[0])

    if location != "" and location != None:
        location = geolocator.geocode(location)
        # print (location)
        distances = {}
        for i in range(100):
            try:
                temp = geolocator.geocode(r[sims[i][1]]["location"])
                distances[i] = geopy.distance.vincenty(location, temp).km
            except:
                distances[i] = 10000000
            

                

        sorted_x = sorted(distances.items(), key=operator.itemgetter(1))
        sims2 = []
        # print (sorted_x)
        for i in sorted_x[:10]:
            sims2.append(sims[i[0]])

        sims = sims2

    data = str(r[sims[0][1]]["jobID"]) + " "

    for i in range(1, 10):
        data += str(r[sims[i][1]]["jobID"]) + " "

    print (data[:-1])
    fin = time.time()
    if args.t:
        print ("Total Time: %s" % (fin - now))
        print ("Loop time: %s" % (loop_now))

    sys.stdout.flush()


parser = argparse.ArgumentParser(description='search')
parser.add_argument('-t', action='store_true')
args = parser.parse_args()

r = requests.get("http://18.220.46.51:3000/api/queries/GetAvailableJobs", headers={"x-api-key": "qLBrEwIv690nAbMfVHB965WC3KfoC1VpvkBjDUiBfVOG5mTzlUlwkckKLerAUxxv"})


r = r.json()

dictionary = corpora.Dictionary.load('data/data.dict')
corpus = corpora.MmCorpus('data/data.mm')

lsi = models.TfidfModel.load("models/model.tfidf")

model = models.Word2Vec.load("models/model.w2v")

index = similarities.MatrixSimilarity(lsi[corpus])


while True:
    term = input()
    d = re.findall(r'"(.*?)"', term)
    term = d[0]
    location = d[1]
    sort_type = d[2]
    # t = time.time()
    loop.run_until_complete(search(term, location, sort_type))
    # print (time.time() - t)

