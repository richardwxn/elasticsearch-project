__author__ = 'newuser'

import ijson

def readTweets(fileName):

    data = open(fileName)

    for item in ijson.items(data, "item.tweet_text"):
          shit.write(item+'\n')
# '''    parser = ijson.parse(data)
#     list(parser)
#     for prefix, event, value in parser:
#         if prefix=="tweet_id":
#
#             print value '''

shit=open('/Users/newuser/Desktop/CS410/ha.txt','w')
readTweets('/Users/newuser/Desktop/CS410/TrainTweets.txt')
