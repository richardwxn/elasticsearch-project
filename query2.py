__author__ = 'newuser'
__author__ = 'newuser'

from elasticsearch import Elasticsearch
import string
import nltk
from nltk.corpus import stopwords
import ijson

cachedStopWords = stopwords.words("english")

def excuteQuery(query):

    es = Elasticsearch()

    r = es.search(
                  index = 'xwen12_bigindex',
                  body ={
                    "query": {
                        "multi_match": {
                            "query": {
                                "query" : query,
                                "fields" : ["body_lmd^3", "body_bm25", "title_lmd^3", "title_bm25^2"],
                                "type":       "most_fields",

                            }
                        }
                    }
                  }
        )

    print r['hits']['total']


    count = 0
    for hit in r['hits']['hits']:

        if(count < 10):
            if(count!=9):
                shit.write(hit['_source']['doc_id'].replace("\n","").replace('"',"").replace(" ",""))
            else:
                shit.write(hit['_source']['doc_id'].replace(",","").replace('"',"").replace(" ",""))
            count += 1
def generateQuery(rawString):

    out = rawString.translate(string.maketrans("",""), string.punctuation)

    out = ' '.join([word for word in out.split() if word not in cachedStopWords])

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
            shit.write(tweetstring[i]+'\t')
            break
        excuteQuery(generateQuery(str(item)))
        i=i+1
    data.close()

shit=open('/Users/newuser/Desktop/CS410/hw3part2/TestPredictions.txt','w+')
readTweets('/Users/newuser/Desktop/CS410/hw3part2/TestTweets.txt')
shit.close()

