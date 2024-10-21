import tweepy
import matplotlib.pyplot as plt
from textblob import TextBlob
import os

def load_env_vars(env_path):
    with open(env_path, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                os.environ[key] = value

# Load environment variables
load_env_vars('.env')

# Twitter API credentials
consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

def fetch_tweets(query, count=100):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = []
    try:
        print("Testing API connection...")
        user = api.verify_credentials()
        print(f"Successfully connected to Twitter API. Authenticated user: @{user.screen_name}")

        print(f"Searching for tweets with query: {query}")
        fetched_tweets = api.search_tweets(q=query, count=count, lang="en", tweet_mode="extended")
        for tweet in fetched_tweets:
            parsed_tweet = {}
            parsed_tweet['text'] = tweet.full_text
            parsed_tweet['sentiment'] = get_tweet_sentiment(tweet.full_text)
            tweets.append(parsed_tweet)
        print(f"Found {len(tweets)} tweets")
        return tweets
    except tweepy.TweepError as e:
        print(f"Error: {str(e)}")
    return None

def get_tweet_sentiment(tweet):
    analysis = TextBlob(tweet)
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'

def analyze_tweets(tweets):
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    
    print(f"Positive tweets percentage: {100*len(ptweets)/len(tweets):.2f}%")
    print(f"Negative tweets percentage: {100*len(ntweets)/len(tweets):.2f}%")
    print(f"Neutral tweets percentage: {100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets):.2f}%")

    return [len(ptweets), len(ntweets), len(tweets) - len(ntweets) - len(ptweets)]

def plot_sentiment(sentiment_counts):
    labels = 'Positive', 'Negative', 'Neutral'
    sizes = sentiment_counts
    colors = ['yellowgreen', 'lightcoral', 'gold']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
    plt.axis('equal')
    plt.title('Sentiment Analysis of Tweets about Campervan Rentals')
    plt.savefig('sentiment_analysis_plot.png')
    plt.close()

# Main execution
if __name__ == "__main__":
    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("Twitter API credentials are not set. Please check your .env file.")
    else:
        print("Twitter API credentials loaded successfully.")
        query = "campervan rental OR RV rental OR motorhome rental"
        print(f"Fetching tweets about: {query}")
        tweets = fetch_tweets(query, count=100)
        
        if tweets:
            print(f"Total tweets analyzed: {len(tweets)}")
            sentiment_counts = analyze_tweets(tweets)
            plot_sentiment(sentiment_counts)
            
            print("\nData visualization saved as 'sentiment_analysis_plot.png'")
            print("\nHow to use this data:")
            print("1. Gauge public sentiment towards campervan rentals")
            print("2. Identify potential customer pain points or positive aspects to inform the Business Launch Decision")
            print("3. Use sentiment trends to guide the Marketing Focus decision")
            print("4. Analyze specific comments to inform Additional Services offerings")
        else:
            print("Failed to fetch tweets. Please check the error messages above for more information.")
