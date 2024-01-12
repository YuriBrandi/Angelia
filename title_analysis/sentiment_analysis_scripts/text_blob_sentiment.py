import pandas as pd
from textblob import TextBlob


def polarization_extraction(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


df = pd.read_csv('../datasets/titles_dataset.csv')
sentiment_score = 0
heuristics_score = 0

for row in df.itertuples():
    real_sentiment = polarization_extraction(row.real_news)
    fake_sentiment = polarization_extraction(row.fake_news)
    if real_sentiment != fake_sentiment:
        sentiment_score += 1
    elif "fake" in row.real_news.lower():
        heuristics_score += 1
    elif row.real_news.lower().startswith("no, "):
        heuristics_score += 1
    elif "false" in row.real_news.lower():
        heuristics_score += 1
    elif row.real_news.lower().startswith("no "):
        heuristics_score += 1
    elif row.real_news.lower().startswith("no."):
        heuristics_score += 1

print(f"sentiment_score {sentiment_score}; in %: {(sentiment_score / len(df)) * 100}.\ntotal_score {sentiment_score + heuristics_score}; in %: {((sentiment_score + heuristics_score) / len(df)) * 100}")
