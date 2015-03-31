__author__ = 'newuser'

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

client = Elasticsearch()

# s = Search(using=client, index="xwen12_bigindex") \
#     .filter("term", title="sport") \
#     .query("match", body="best")
    # .query(~Q("match", body="soccer"))

# s.aggs.bucket('per_tag', 'terms', field='tags') \
#     .metric('max_lines', 'max', field='lines')

body={
  "query": {
    "custom_filters_score": {
      "query": {"best player" },
      "filters": [
        {
          "filter": {
            "term": {
              "title": "sport"
            }
          },
          "boost": 1.3
        },
        {
          "filter": {
            "term": {
              "title": "bad"
            }
          },
          "boost": 1.2
        },
        {
          "filter": {
            "and": [
              {
                "term": {
                  "type": "worst"
                }
              }
            ]
          },
          "boost": 0.2
        }
      ],
      "score_mode": "multiply"
    }
  }
}
s = Search.from_dict(body)

# Add some filters, aggregations, queries, ...
s.filter("term", title="sport")

# Convert back to dict to plug back into existing code
# body = s.to_dict()
response = s.execute()

for hit in response:
    print(hit._meta.score, hit.title)

# for tag in response.aggregations.per_tag.buckets:
#     print(tag.key, tag.max_lines.value)