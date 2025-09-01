from elasticsearch import Elasticsearch, helpers
import pandas as pd
import os
HOST = os.environ.get('ELASTICSEARCH_HOST')
PORT = os.environ.get('ELASTICSEARCH_PORT')
class GetElastic:
    def __init__(self):
        self.es = Elasticsearch(HOST)
        self.index_name = 'antisemitic_tweets'
        self.query = None
    def read_all(self,query):
        query ={
            "query": {query: {}}
        }
        results = helpers.scan(self.es,index=self.index_name, body=query)
        return results

# read = GetElastic()
# a = read.read_index(read.index_name,'match_all')
# print(a)
