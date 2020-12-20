from afinn import Afinn
afinn = Afinn(language='en')

silmarillion_sentiments['afinn_score'] = silmarillion_sentiments['text'].apply(afinn.score)

sentiment_scores = silmarillion_sentiments['afinn_score']
silmarillion_sentiments['afinn_category'] = ['Positive' if score > 0 
                          else 'Negative' if score < 0 
                              else 'Neutral' 
                                  for score in sentiment_scores]
