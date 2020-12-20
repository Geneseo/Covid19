import pandas as pd
import nltk
from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer
lemma = nltk.wordnet.WordNetLemmatizer()
from nltk.stem import WordNetLemmatizer
wordnet_lemmatizer = WordNetLemmatizer()
from tqdm import tqdm_notebook as tqdm
from tqdm import trange

def text_emotion(df, column):
    new_df = df.copy()

    filepath = ('NRC-Emotion-Lexicon-Wordlevel-v0.92.txt') 
    emolex_df = emolex_df = pd.read_csv(filepath,
                                        names=["word", "emotion", "association"],
                                        skiprows=45, sep='\t', keep_default_na=False)
    emolex_words = pd.read_csv("NRCemolex_words.csv")

    emotions = emolex_words.columns.drop('word') # list of emotions
    emo_df = pd.DataFrame(0, index=df.index, columns=emotions)

    with tqdm(total=len(list(new_df.iterrows()))) as pbar:
        for i, row in new_df.iterrows():
            pbar.update(1)
            document = word_tokenize(new_df.loc[i][column])
            for word in document:
                word = wordnet_lemmatizer.lemmatize(word, pos="v")
                emo_score = emolex_words[emolex_words['word'] == word]
                if not emo_score.empty:
                    for emotion in list(emotions):
                        emo_df.at[i, emotion] += emo_score[emotion]

    new_df = pd.concat([new_df, emo_df], axis=1)

    return new_df

#silmarillion_sentiments_finalized = text_emotion(silmarillion_sentiments, 'text')

#Calculate happiness mean
import matplotlib.pylab as plt
from wordshifts import Sentiment
from wordshifts import WordShifts

wShift = WordShifts()
sentiment = Sentiment()

def happiness_mean(text):
    return sentiment.compute(text)['happiness_mean']

data_geofips['happiness_mean'] = data_geofips.apply(lambda row: happiness_mean(row['text']), axis=1)

    
