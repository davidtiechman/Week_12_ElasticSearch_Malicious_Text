from elasticsearch import Elasticsearch, helpers
import pandas as pd
import logging
import os


HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost')
PORT = (os.environ.get('ELASTICSEARCH_PORT', '9200'))
ELASTIC_URL = f"http://{HOST}:{PORT}"

class GetElastic:
    def __init__(self):
        self.es = Elasticsearch(ELASTIC_URL)
        self.index_name = 'antisemitic_tweets'
        self.query = None
    def read_all(self,query):
        logging.info(f'reading query {query}')
        query ={
            "query": {query: {}}
        }
        results = helpers.scan(self.es,index=self.index_name, body=query)
        logging.info(f'successfully read query {query}')
        return results
