import os
import tweepy
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from linebot.models import (
    TextSendMessage, ImageSendMessage, VideoSendMessage
)

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')


# twitter で#松岡茉優の画像検索してURL取得
def search_tweets():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    yesterday = datetime.strftime(
        datetime.today() - relativedelta(days=1), f"%Y-%m-%d")

    q = f"#松岡茉優 OR 松岡茉優 -'松岡茉優似' filter:media exclude:retweets min_faves:10 since:{yesterday} min_retweets:0"

    tweets = tweepy.Cursor(
        api.search,
        q=q,
        tweet_mode='extended',
        result_type="mixed",
        include_entities=True,
    ).items(20)

    contents = []
    for tweet in tweets:
        print(tweet.full_text)
        try:
            media = tweet.extended_entities['media']
            print(media)
            for m in media:
                print(m)
                preview = m['media_url_https']
                if m['type'] == 'video':
                    origin = [variant['url'] for variant in m['video_info']
                              ['variants'] if variant['content_type'] == 'video/mp4'][0]
                else:
                    origin = m['media_url_https']

                content = {'preview': preview,
                           'origin': origin, 'type': m['type']}
                contents.append(content)

            print('--------------------------------------------')
        except:
            print('noUrl')
            print('--------------------------------------------')

    messages = []
    for media in contents:
        item = VideoSendMessage(
            original_content_url=media['origin'], preview_image_url=media['preview']) if media['type'] == 'video' else ImageSendMessage(
            original_content_url=media['origin'], preview_image_url=media['preview'])

        messages.append(item)

    return [messages[0:5], messages[5:10]]


if __name__ == "__main__":
    search_tweets()
