## 1.Vader 
import pandas as pd
from nltk import tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 


chapters = data_geofips["text"].tolist()

analyzer = SentimentIntensityAnalyzer()

sentiments_list = list()

for chapter in chapters:
    sentence_list = tokenize.sent_tokenize(chapter)
    sentiments = {'compound': 0.0, 'neg': 0.0, 'neu': 0.0, 'pos': 0.0}
        
    for sentence in sentence_list:
        vs = analyzer.polarity_scores(sentence)
        sentiments['compound'] += vs['compound']
        sentiments['neg'] += vs['neg']
        sentiments['neu'] += vs['neu']
        sentiments['pos'] += vs['pos']
            
    sentiments['compound'] = sentiments['compound'] / len(sentence_list) if len(sentence_list)>0 else None
    sentiments['neg'] = sentiments['neg'] / len(sentence_list) if len(sentence_list)>0 else None
    sentiments['neu'] = sentiments['neu'] / len(sentence_list) if len(sentence_list)>0 else None
    sentiments['pos'] = sentiments['pos'] / len(sentence_list) if len(sentence_list)>0 else None
    
    sentiments_list.append(sentiments)  # add this line

data4 = pd.DataFrame(sentiments_list)  # add this line
data4

# perform each data from feb to may
data_geofips.reset_index(inplace = True)

silmarillion_sentiments = pd.merge(data_geofips, data4, left_index=True, right_index=True)
silmarillion_sentiments=silmarillion_sentiments.rename(columns={"compound": "VD_Compound", "neg": "VD_Negative", "neu": "VD_Neutral", "pos": "VD_Positive"})

def rating(silmarillion_sentiments):
    if silmarillion_sentiments['VD_Compound'] > 0.05:
        return 'Positive'
    elif silmarillion_sentiments['VD_Compound'] < -0.05:
        return 'Negative'
    else:
        return 'Neutral'

silmarillion_sentiments['Rating'] = silmarillion_sentiments.apply(rating, axis=1)

silmarillion_sentiments.head(10)
