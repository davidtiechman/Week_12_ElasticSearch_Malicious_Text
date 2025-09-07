from convert_to_object import convert_to_df, convert_to_dict
from load_data.load_file import load_file_csv, write_json
from connect_elastics.index_documents import IndexElasticsearch
from connect_elastics.get_elastics import GetElastic
import pandas as pd
from processing.analysis import Processing

def run_pipeline():
    csv = load_file_csv('tweets_injected 3.csv')
    dictionary = convert_to_dict(csv)
    insert = IndexElasticsearch('antisemitic_tweets')
    insert.insert_collect(dictionary)
    get_elastic = GetElastic()
    results_all = get_elastic.read_all('match_all')
    a_list =  list(results_all)
    df = pd.json_normalize(a_list,sep='_')
    print(f'teh sum document is {len(df)}')
    proces = Processing(df,'_source_text')
    proces.emotion_analysis()
    proces.division_text()
    proces.convert_text_to_lowercase()
    df = proces.find_weapon_name()
    insert.update_collect(df,'type_text')
    insert.update_collect(df,'weapons_detected')
    query = {
    "query": {
        "bool": {
            "must": [
                {"term": {"Antisemitic": 0}},
                {"terms": {"type_text": ["neutral", "positive"]}}
            ],
            "must_not": [
                {"exists": {"field": "weapons_detected"}}  # אם רוצים ריקים
            ]
        }
    }
    }
    insert.delete_collect(query)
    new_get = GetElastic()
    new_results = new_get.read_all('match_all')
    a_list = list(new_results)
    new_df = pd.json_normalize(a_list,sep='_')
    print(f'the sum document is {len(new_df)}')
    return True
