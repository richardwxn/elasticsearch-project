# -*- coding: utf-8 -*-
__author__ = 'newuser'

from elasticsearch import Elasticsearch
import string
import nltk
from nltk.corpus import stopwords
import ijson
import re
import enchant
from nltk.stem.lancaster import LancasterStemmer

cachedStopWords = stopwords.words("english")

def excuteQuery(query):

    es = Elasticsearch()

    # r = es.search(index = 'xwen12_bigindex', q = query)

    r = es.search(index = 'xwen12_bigindex', q = query)

    # r=es.search(index="xwen12-bigindex", fields="body", body={"function_score": {
    #     "query": {
    #         { "match": {"body": {"query":query} }
    #     },
    #     "functions": {
    #         "DECAY_FUNCTION": {
    #             "recencyboost": {
    #                 "origin": "0",
    #                 "scale": "20"
    #             }
    #         }
    #     },
    #     "score_mode": "multiply"
    # })

    print r['hits']['total']


    count = 0
    for hit in r['hits']['hits']:

        if(count < 10):
            if(count!=9):
                shit.write(hit['_source']['doc_id'].replace('"',"").replace(" ","").replace("\n",""))
            else:
                shit.write(hit['_source']['doc_id'].replace(",","").replace('"',"").replace(" ",""))
            count += 1
def generateQuery(rawString):
    # out = re.sub(r'''(?i)\b((?:http?://\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|
    #              (\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’]))''', '', rawString)
    out = rawString.translate(string.maketrans("",""), string.punctuation)

    out = ' '.join([word for word in out.split() if word not in cachedStopWords])
    # out = out.split("http")[0]
    # = LancasterStemmer()st
    # d = enchant.Dict("en_US")
    # out = ' '.join([st.stem(word) for word in out.split()])
    # out = ' '.join([word for word in out.split() if d.check(word)==True])


    print(out)
    return out

def readTweets(fileName):

    data = open(fileName)
    tweetstring=[]
    i=0
    for tweet in ijson.items(data, 'item.tweet_id'):
        tweetstring.append(str(tweet))
        print(tweet+'\n'+str(i))
        i=i+1
    data.close()
    data=open(fileName)
    i=0
    for item in ijson.items(data, 'item.tweet_text'):
        while(i<len(tweetstring)):
            shit.write(tweetstring[i].rstrip('\n')+'\t')
            break
        # for lines in shit:
        #     shit.wrtie(lines.replace("\n", 'aa'))
        excuteQuery(generateQuery(str(item)))
        i=i+1
    data.close()

shit=open('/Users/newuser/Desktop/CS410/hw3part2/TestPredictions.txt','r+')

readTweets('/Users/newuser/Desktop/CS410/hw3part2/TestTweets.txt')
shit.close()
