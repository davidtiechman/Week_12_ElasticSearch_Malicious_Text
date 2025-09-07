from elasticsearch import Elasticsearch, helpers
import logging
import time
import os

HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost')
PORT = os.environ.get('ELASTICSEARCH_PORT', '9200')
ELASTIC_URL = f"http://{HOST}:{PORT}"

class IndexElasticsearch:
    def __init__(self,index_name):
        self.index_name = index_name
        self.es = None
        for i in range(10):
            try:
                self.es = Elasticsearch(ELASTIC_URL)
                if self.es.ping():
                    logging.info(f"Connected to Elasticsearch")
                    break
                time.sleep(3)
            except Exception as e:
                logging.error(f"Failed to connect to Elasticsearch: {e}")

    def insert_collect(self,collection):
        logging.info(f'inserting {collection}')
        actions = [{'_index' : self.index_name,
            '_id' : i+1,'_source' : doc}
            for i, doc in enumerate(collection)]
        try:
            helpers.bulk(self.es, actions)
            logging.info(f'successfully inserted {collection}')
        except helpers.BulkIndexError as e:
            for error in e.errors:
                print(error)

    def update_collect(self,df,new_field):
        logging.info(f'updating {new_field}')
        actions = [
            {'_op_type': 'update',
             '_index' : self.index_name,
             '_id' : row['_id'],
             'doc': {new_field: row[new_field],}
             }
            for _, row in df.iterrows()
        ]
        try:
            helpers.bulk(self.es, actions)
            logging.info(f'successfully updated {new_field}')
            print('the collection index has been indexed')
        except helpers.BulkIndexError as e:
            print(e)
    def delete_collect(self,query):
        logging.info(f'deleting {query}')
        try:
            self.es.delete_by_query(index=self.index_name, body=query)
            logging.info(f'successfully deleted {query}')
            print('the collection index has been deleted')
        except Exception as e:
            print(e)
#
docs = [{'title': 'document 1', "content": "content 1"},
    {'title': 'document 2', "content": "content 2"},
    {'title': 'document 3', "content": "content 3"}]
a = IndexElasticsearch(docs)
a.insert_collect('my_el')