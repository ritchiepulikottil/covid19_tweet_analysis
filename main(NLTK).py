import string
from nltk.tokenize import word_tokenize
from collections import Counter
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt

import GetOldTweets3 as got
def get_tweets():
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch('corona')\
                                           .setSince("2019-08-29")\
                                           .setUntil("2020-08-29")\
                                           .setMaxTweets(1000)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)
    text_tweets = [[tweet.text] for tweet in tweets]
    return text_tweets 


txt = ""
text_tweets = get_tweets()
length = len(text_tweets)
for i in range(0, length):
    txt = text_tweets[i][0]+" " + txt
    
lcase = txt.lower()
clean = lcase.translate(str.maketrans("","",string.punctuation))
seperate = word_tokenize(clean, "english")


req = []
for i in seperate:
    if i not in stopwords.words("english"):
        req.append(i)
        

emolist = []
fh = open("emotions.txt")
for line in fh:
    strip = line.strip().replace("'","").replace(",", "")
    m,n = strip.split(":")
    if m in req :
        emolist.append(n)

w = Counter(emolist)
print(w)
fig, ax1 = plt.subplots()
def sentiment_analyze(sentiment_text):
    score = SentimentIntensityAnalyzer().polarity_scores(sentiment_text)
    neg = score["neg"]
    pos = score["pos"]
    if neg>pos:
        fig.suptitle('CORONA TWEET ANALYSIS \n OVERALL RESULT : NEGATIVE SENTIMENT', fontsize=14, fontweight='bold')
    elif pos>neg:
        fig.suptitle('CORONA TWEET ANALYSIS \n OVERALL RESULT : POSITIVE SENTIMENT', fontsize=14, fontweight='bold')
    else:
        fig.suptitle('CORONA TWEET ANALYSIS \n OVERALL RESULT : NEUTRAL SENTIMENT', fontsize=14, fontweight='bold')
        
sentiment_analyze(clean)
ax1.bar(w.keys(), w.values())
fig.autofmt_xdate()

plt.savefig("result.png")
plt.show()





