from elasticsearch import Elasticsearch, helpers
import os

HOST = os.environ.get('ELASTICSEARCH_HOST', 'localhost')
PORT = (os.environ.get('ELASTICSEARCH_PORT', '9200'))

class IndexElasticsearch:
    def __init__(self,index_name):
        self.es =  Elasticsearch(HOST)
        self.index_name = index_name
        # self.index_name = None

    def insert_collect(self,collection):
        actions = [{'_index' : self.index_name,
            '_id' : i+1,'_source' : doc}
            for i, doc in enumerate(collection)]
        try:
            helpers.bulk(self.es, actions)
        except helpers.BulkIndexError as e:
            for error in e.errors:
                print(error)

    def update_collect(self,df,new_field):
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
            print('the collection index has been indexed')
        except helpers.BulkIndexError as e:
            print(e)
    def delete_collect(self,query):
        try:
            self.es.delete_by_query(index=self.index_name, body=query)
            print('the collection index has been deleted')
        except Exception as e:
            print(e)

# docs = [{'title': 'document 1', "content": "content 1"},
#     {'title': 'document 2', "content": "content 2"},
#     {'title': 'document 3', "content": "content 3"}]
# a = IndexElasticsearch(docs)
# a.index_doc('new_ind')