from elasticsearch import Elasticsearch
import pandas as pd
from config import HOST
class GetElastic:
    def __init__(self):
        self.es = Elasticsearch(HOST)
        self.query = None
    def read_index(self,index_name,query):
        query ={
            "query": {
                f'{query}': {}
            }
        }
        results =  self.es.search(index=index_name, body=query)
        return results

# read = GetElastic()
# a = read.read_index('new_ind','match_all')
# print(a)
