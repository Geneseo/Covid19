# Project Title

# Covid19_ Sentiment Analysis



# COVID-19-TweetIDs 
The repository contains an ongoing collection of tweets IDs associated with the novel coronavirus COVID-19 (SARS-CoV-2), which commenced on January 28, 2020. We used the Twitter’s search API to gather historical Tweets from the preceding 7 days, leading to the first Tweets in our dataset dating back to January 21, 2020.
The data is available at * [github](https://github.com/echen102/COVID-19-TweetIDs#covid-19-tweetids)

# How to Hydrate
I used Twarc package to hydrate all Tweet-IDs stored in their corresponding folders. Install Twarc first.

```
pip3 install twarc
```

## Description of folder
* **getRawTweet** - Using Twarc, I get Tweet data in Json format. I converted json file to csv format.  
* **preprocessing** - Load csv files and clean data. Using API, It assign fips code to each tweet. (We only use tweet which has geo-coordinate)  
* **SentimentAnalysis** - We performed sentiment analysis using 1.Vader 2.Nrc_Lexicon 3. Afinn
* **SummaryReport** - This include summary statistics of sentiment difference by state and wordcloud.  
* **external_data** - Health policy by state [github](https://github.com/COVID19StatePolicy/SocialDistancing)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
