import nltk
from nltk.sentiment import vader
from load_data.load_file import load_file_txt

class Processing:
    def __init__(self,df,column_text):
        self.df = df
        self.column_text = column_text
    def emotion_analysis(self):
        nltk.download('vader_lexicon')
        analyzer = vader.SentimentIntensityAnalyzer()
        self.df['score'] = self.df[self.column_text].apply(lambda text: analyzer.polarity_scores(str(text))['compound'])
        self.df['type_text'] = self.df['score'].apply(lambda s: 'positive' if s >= 0.5 else ('negative' if s <= -0.5 else 'neutral'))
        self.df.drop(columns=['score'], inplace=True)
        return self.df

    def division_text(self):
        self.df['list_words'] = self.df[self.column_text].str.split()
        return self.df

    def convert_text_to_lowercase(self):
        self.df[self.column_text] = self.df[self.column_text].apply(lambda x: x.lower())
        return self.df

    def find_weapon_name(self):
        self.df['weapons_detected'] = self.df.apply(self.lop_of_array_weapons, axis=1)
        return self.df

    def lop_of_array_weapons(self,row):
        arr_weapon = load_file_txt('weapon_list (1).txt')
        arr_weapon = [w.lower() for w in arr_weapon]
        found_weapons = [w for w in arr_weapon if w in row[self.column_text]]
        return found_weapons if found_weapons else " "