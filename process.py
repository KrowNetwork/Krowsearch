import pandas as pd
import numpy as np
import logging, gensim
from gensim import similarities, corpora
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

df = pd.read_csv('data job posts.csv')
df.drop_duplicates()
df.reset_index(drop=True)
# print (df.columns)
# print (df['jobpost'][0])
np.random.shuffle(df.values)
documents = df['Title']
# titles = df['title']
# companies = list(df['company'].values)
stoplist = list(set('for a of the and to in at • is will on as our or we an work new with you are be · all other inc your about becasue that their this too each few during has by job'.split()))
texts = [[word for word in str(document).lower().split() if word not in stoplist] for document in documents]
#
# titles_ = [[word for word in str(title).lower().split() if word not in stoplist] for title in titles]
#
# comapnies_ = [[word for word in str(company).lower().split() if word not in stoplist] for company in companies]
#
# titles = titles_
# companies = comapnies_
# count = 0
# for i in texts:
#     i.extend(titles[count])
#     i.extend(companies[count])
#     count += 1
# # texts.extend(title)
# # print (companies)
# # texts.extend([companies])
# # texts[0].extend(companies)
# # remove words that appear only once
# # from collections import defaultdict
# # frequency = defaultdict(int)
# # for text in texts:
# #     for token in text:
# #         frequency[token] += 1
# #
# # texts = [[token for token in text if frequency[token] > 1]
# #          for text in texts]
# print (texts)
# # dictionary = corpora.Dictionary(texts)
# # dictionary.save('test.dict')
# # corpus = [dictionary.doc2bow(text) for text in texts]
# # corpora.MmCorpus.serialize('test.mm', corpus)
#
dictionary = corpora.Dictionary(texts)
dictionary.save('data.dict')
corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('data.mm', corpus)
