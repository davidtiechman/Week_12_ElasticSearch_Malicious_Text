from convert_to_df import convert_to_df
from load_data.load_file import load_file_csv, write_json
from index_documents import IndexElasticsearch
from processing.analysis import emotion_analysis

csv = load_file_csv('data/tweets_injected 3.csv')
js = write_json('.data/tweets_json.json',csv)
i = IndexElasticsearch()
i.index_collect('tweets',js)