# import tweepy
# from textblob import TextBlob
# import pandas as pd

# # Step 1 - Authenticate
# consumer_key= 'PvQ3Rg5zEgrxLtuFvMIa6CZBR'
# consumer_secret= 'c4dtWS4U8JqF460iHBesRcHp9EMfqXelASXtTPSRaCKd4CqgNt'

# access_token='898962735886618624-iOEgYEOFPQvSCHGuxz3Mc344fBoYyGS'
# access_token_secret='Gh9s1I3Wk8AljBq8kymJi7xjk4rhYEyedRTntjYbNe6j2'

# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token, access_token_secret)

# api = tweepy.API(auth)

# #Step 3 - Retrieve Tweets
# public_tweets = api.search('Trump')
# df = 


# #CHALLENGE - Instead of printing out each tweet, save each Tweet to a CSV file
# #and label each one as either 'positive' or 'negative', depending on the sentiment 
# #You can decide the sentiment polarity threshold yourself


# for tweet in public_tweets:
#     print(tweet.text)
    
#     #Step 4 Perform Sentiment Analysis on Tweets
#     analysis = TextBlob(tweet.text)
#     print(analysis.sentiment)
#     print("")

import tweepy
from textblob import TextBlob
#French adaptor
from textblob_fr import PatternTagger, PatternAnalyzer

import numpy as np
import operator


# Step 1 - Authenticate
consumer_key= 'PvQ3Rg5zEgrxLtuFvMIa6CZBR'
consumer_secret= 'c4dtWS4U8JqF460iHBesRcHp9EMfqXelASXtTPSRaCKd4CqgNt'

access_token='898962735886618624-iOEgYEOFPQvSCHGuxz3Mc344fBoYyGS'
access_token_secret='Gh9s1I3Wk8AljBq8kymJi7xjk4rhYEyedRTntjYbNe6j2'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

#Step 2 - Prepare query features

#List of candidates to French Republicans Primary Elections
candidates_names = ['Narendra Modi', 'Rahul Gandhi', 'Ronaldo', 'Messi', 'Hazard', 'Mason Mount']
# #Hashtag related to the debate
# name_of_debate = "PrimaireLeDebat" 
# #Date of the debate : October 13th
# since_date = "2016-10-13"
# until_date = "2016-10-14"

#Step 2b - Function of labelisation of analysis
def get_label(analysis, threshold = 0):
	if analysis.sentiment[0]>threshold:
		return 'Positive'
	else:
		return 'Negative'


#Step 3 - Retrieve Tweets and Save Them
all_polarities = dict()
for candidate in candidates_names:
	this_candidate_polarities = []
	#Get the tweets about the debate and the candidate between the dates
	this_candidate_tweets = api.search(candidate)
	# print(len(this_candidate_tweets))
	#Save the tweets in csv
	with open('%s_tweets.csv' % candidate, 'w') as this_candidate_file:
		this_candidate_file.write('tweet,sentiment_label\n')
		for tweet in this_candidate_tweets:
			analysis = TextBlob(tweet.text)
			#Get the label corresponding to the sentiment analysis
			this_candidate_polarities.append(analysis.sentiment)
			this_candidate_file.write('%s,%s\n' % (tweet.text.encode('utf8'), get_label(analysis)))
	#Save the mean for final results
	all_polarities[candidate] = np.mean(this_candidate_polarities)
 
#Step bonus - Print a Result
sorted_analysis = sorted(all_polarities.items(), key=operator.itemgetter(1), reverse=True)
print ('Mean Sentiment Polarity in descending order :')
for candidate, polarity in sorted_analysis:
	print ('%s : %0.3f' % (candidate, polarity))
