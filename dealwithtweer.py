__author__ = 'newuser'

from elasticsearch import Elasticsearch
from elasticsearch import helpers
import timeit
import ijson
import stream

#!/usr/bin/env python

import io
import json
import re
import textwrap
from collections import defaultdict

import click
import elasticsearch


@click.command()
@click.argument('query', required=True)
@click.option('--raw-result/--no-raw-result', default=False)
query="best school program"
def search(query, raw_result):
    fulltext = io.StringIO()
    keywords = defaultdict(str)
    for token in query.split():
        idx = token.find(':')
        if 0 <= idx < len(token):
            key, value = token.split(':', 1)
            keywords[key] += ' ' + value
        else:
            fulltext.write(' ' + token)

    q = {
        'query': {
            'bool': {
                'must': [{'match': {k: v}} for k, v in keywords.viewitems()]
            }
        }
    }

    fulltext = fulltext.getvalue()
    if fulltext:
        q['query']['bool']['should'] = [{'match': {'contents': fulltext}}]

    es = elasticsearch.Elasticsearch()
    matches = es.search('mail', 'message', body=q)
    hits = matches['hits']['hits']
    if not hits:
        click.echo('No matches found')
    else:
        if raw_result:
            click.echo(json.dumps(matches, indent=4))
        for hit in hits:
            click.echo(textwrap.dedent('''\
                Subject: {}
                From: {}
                To: {}
                Content: {}...
                Path: {}
                '''.format(
                hit['_source']['subject'],
                hit['_source']['from'],
                hit['_source']['to'],
                re.sub(r'[\r\n\t]', ' ', hit['_source']['contents'])[:80],
                hit['_source']['path']
            )))

if __name__ == '__main__':
    search()
