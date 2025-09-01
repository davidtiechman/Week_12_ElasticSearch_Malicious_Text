from wsgiref import headers
import pandas as pd

def convert_to_df(js):
    df = pd.DataFrame(js)
    return df

def convert_to_dict(list_tweets):
    headers = list_tweets[0]
    rows = list_tweets[1:]
    dictionary  = [dict(zip(headers, row)) for row in rows]
    return dictionary

