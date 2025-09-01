from elasticsearch import Elasticsearch, helpers
from config import HOST
class IndexElasticsearch:
    def __init__(self):
        self.es = Elasticsearch(HOST)
        # self.collection = docs
        # self.index_name = None

    def index_collect(self,index_name,collection):
        actions = [{'_index' : index_name,
            '_id' : i+1,'_source' : collection}
            for i, doc in enumerate(collection)]
        helpers.bulk(self.es, actions)
        print('the collection index has been indexed')

    def index_doc(self,new_index,id_field=None):
        self.index_name = new_index
        if not self.es.indices.exists(index=self.index_name):
            self.es.indices.create(index=self.index_name)
        for i, doc in enumerate(self.collection):
            doc_id = doc.get(id_field)
            self.es.index(index=new_index,id=doc_id,body=doc)
            if i % 100 == 0:
                print(f'{i} docs indexed')
        print('the collection index has been indexed')

# docs = [{'title': 'document 1', "content": "content 1"},
#     {'title': 'document 2', "content": "content 2"},
#     {'title': 'document 3', "content": "content 3"}]
# a = IndexElasticsearch(docs)
# a.index_doc('new_ind')