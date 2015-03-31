__author__ = 'newuser'
__author__ = 'newuser'



from datetime import datetime
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import timeit
import ijson
from ijson import items



start = timeit.default_timer()
sb = open("/Users/newuser/Desktop/CS410/hw3part2/Docs.txt")
#k = open("/Users/newuser/Downloads/shit.txt","w")
#parser = ijson.parse(sb)

#for prefix, event, value in parser:
#    if (prefix) == ('url'):
#        k.writelines(value)

#objects = ijson.items(sb, 'doc_id')
# k.close()
lines = sb.readlines()
print lines.__len__()
length = lines.__len__()
es = Elasticsearch()
start=timeit.default_timer()

def indexing():
    actions = []
    s = length-1
    i  = 0
    while i < s:

        action = {
            "_index": "xwen12_bigindex",
            "_type": "doc",
            "url": lines[i].replace("[{\"url\":", ""),
            "body": lines[i+1].replace("\"body\":", ""),
            "doc_id": lines[i+2].replace("\"doc_id\":", ""),
            "title" : lines[i+3].replace("\"title\":", "").replace("},",""),


            }

        i += 4
        actions.append(action)
    helpers.bulk(es, actions)

indexing()



stop = timeit.default_timer()

print stop - start
# bulk index the data



# sanity check
# print("searching...")
# res = es.search(index = "xwen12_index", size=2, body={"query": {"match_all": {}}})

