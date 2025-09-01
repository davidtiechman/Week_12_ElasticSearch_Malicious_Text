import nltk
from nltk.sentiment import vader


def emotion_analysis(df):
    nltk.download('vader_lexicon')  # Compute sentiment labels
    # tweet = self.df['Text'].loc[0]
    df['score'] = df['text'].apply(
        lambda text: vader.SentimentIntensityAnalyzer().polarity_scores(str(text))['compound'])
    df['type_text'] = df['score'].apply(
        lambda s: 'positive' if s >= 0.5 else ('negative' if s <= -0.5 else 'neutral'))
    df.drop(columns=['score'], inplace=True)
    return df