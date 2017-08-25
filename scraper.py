import sys
from textblob import TextBlob
import twitter
import datetime
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.dates as mdates


## Scrapes Tweets using Twitter API and performs sentiment analysis
## Uses packages python-twitter and TextBlob

api = twitter.Api(consumer_key='MN9DU1P8doErgFPCBsbATbonk',
                      consumer_secret='mDxQSkJqedmrvRYCY5uPPxCbbGm7vrG9p5jg6M4pZR4TjJezd9',
                      access_token_key='900731370762379265-AiRKKS9HELTZE7EuIMEhCBj4c98TL2v',
                      access_token_secret='FKZFESWMM24EYjOmudejT9jXpCL0KiLp32jeSTs3uEEfb')



# Parse command line
# python scraper.py [twitter user name] [# of tweets up to 200]
# ex. >> python scraper.py muhrell 200
args = sys.argv


# Get last 10 statuses of input username
twitter_username = args[1]
num_tweets = int(args[2])
try:
	statuses = api.GetUserTimeline(screen_name=twitter_username, count=num_tweets)
except:
	print "Invalid Twitter Username"


monthmap = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6, 'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}



# Parse the Status objects
dates = []
polarities = []
for s in statuses:
    # Uncomment below to print the contents of the tweets
    status_text = s.text
    status_time = s.created_at
	# print '\n' + status_time
	# print s.text
    fav_count = s.favorite_count
    retweet_count = s.retweet_count
	# print "Favorite Count: " + str(fav_count)
	# print "Retweet Count" + retweet_count

    # Run sentiment analysis using TextBlob
    tb = TextBlob(status_text)
    status_polarity = tb.sentiment.polarity
    polarities.append(status_polarity)

    # Parse and format the date/time of the tweet
    split_time = status_time.split(" ")
    dt = datetime.datetime(int(split_time[5]), monthmap[split_time[1]], int(split_time[2]), 0, 0)
    dates.append(dt)


# Create numpy arrays for dates and polarities of the tweets
date_array = np.array([dt for dt in dates])
polarities_array = np.array(polarities)

# Aggregate tweets that are on the same date and take average polarity
def avg_by_day(dates, polarities):
    result_dates = np.unique(dates)
    result_polarities = np.empty(result_dates.shape)

    for i, date in enumerate(result_dates):
        result_polarities[i] = np.mean(polarities[dates == date])

    return result_dates, result_polarities

(date_array, polarities_array) = avg_by_day(date_array, polarities_array)


# Set the plot style
plt.style.use('ggplot')

# Configure matplotlib settings
fig = plt.figure()
output_plot = fig.add_subplot(111)
output_plot.set_title(twitter_username)
output_plot.set_xlabel('Date')
output_plot.set_ylabel('Average Tweet Polarity')
output_plot.xaxis.set_major_formatter(mdates.DateFormatter("%d\n%b\n%Y"))
_=plt.xticks(rotation=90)
output_plot.tick_params(axis='both', which='major', labelsize=7)
output_plot.plot(date_array,polarities_array)

plt.show()
