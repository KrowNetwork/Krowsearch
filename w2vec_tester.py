from gensim import similarities, corpora, models
import argparse
import numpy as np

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

parser = argparse.ArgumentParser(description='search')
parser.add_argument('--similarity',
                    nargs=2, default=[None, None])

args = parser.parse_args()

if (args.similarity != [None, None]):
    model = models.Word2Vec.load("model.w2v")
    print ("Loaded Word2Vec")

    # print (model.wv.wmdistance(args.similarity[0], args.similarity[1]))
    print ("software developer vs financial analyst (FAR): %s" % get_sentence_difference("software developer", "financial analyst", model))
    print ("marketing manager vs financial advisor (CLOSE): %s" % get_sentence_difference("marketing manager", "financial advisor", model))
    print ("%s vs %s: %s" % (args.similarity[0], args.similarity[1], get_sentence_difference(args.similarity[0], args.similarity[1], model)))
