#!/usr/bin/env python3
"""
ThumbnailAI Twitter/X Monitor Bot
Monitors Twitter for thumbnail-related tweets and auto-replies with helpful tips
"""

import tweepy
import schedule
import time
import os
from datetime import datetime

# Twitter API credentials (get at https://developer.twitter.com)
client = tweepy.Client(
    bearer_token=os.getenv("TWITTER_BEARER_TOKEN"),
    consumer_key=os.getenv("TWITTER_API_KEY"),
    consumer_secret=os.getenv("TWITTER_API_SECRET"),
    access_token=os.getenv("TWITTER_ACCESS_TOKEN"),
    access_token_secret=os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
    wait_on_rate_limit=True
)

# Keywords to monitor
KEYWORDS = [
    "YouTube thumbnail",
    "thumbnail designer",
    "thumbnail maker",
    "thumbnail help",
    "CTR help",
    "youtube CTR",
    "thumbnail art",
    "need thumbnail"
]

# Accounts to monitor (YouTube creators who might need thumbnails)
TARGET_ACCOUNTS = [
    "@YouTube",
    "@TeamYouTube",
    "@VidIQ",
    "@Buffer",
    "@LaterMedia",
]

# Helpful reply template
REPLY_TEMPLATE = """
Thumbnails are so important for CTR! A few tips:

• High contrast + bold colors
• Expressive faces (shock/excitement work great)
• 3-5 words max for text overlay
• Test multiple versions!

There are some cool AI tools now that can generate thumbnails in ~60 sec if you want to try A/B testing without the cost of a designer. Good luck! 🚀
"""

def is_valid_tweet(tweet):
    """Filter out tweets we shouldn't reply to"""
    # Skip if tweet is from a verified account (less likely to need help)
    # Skip if tweet is a retweet
    # Skip if we already replied

    return True  # Simplified for now

def monitor_keywords():
    """Monitor Twitter for keyword mentions"""
    print(f"[{datetime.now()}] Starting Twitter keyword monitoring...")

    for keyword in KEYWORDS:
        try:
            # Search recent tweets
            query = f"{keyword} -filter:retweets lang:en"
            tweets = client.search_recent_tweets(
                query=query,
                max_results=10,
                tweet_fields=["author_id", "created_at", "public_metrics"]
            )

            if tweets.data:
                for tweet in tweets.data:
                    # Check if tweet is recent (last 24 hours)
                    tweet_age = datetime.now() - tweet.created_at.replace(tzinfo=None)
                    if tweet_age.total_seconds() < 86400:  # 24 hours
                        print(f"\n✅ Found tweet: {tweet.text[:100]}...")
                        print(f"URL: https://twitter.com/i/status/{tweet.id}")
                        print(f"Likes: {tweet.public_metrics['like_count']}, Retweets: {tweet.public_metrics['retweet_count']}")
                        print("-" * 50)

        except Exception as e:
            print(f"Error searching '{keyword}': {e}")

    print(f"[{datetime.now()}] Keyword monitoring complete.\n")

def monitor_accounts():
    """Monitor target accounts for replies we can join"""
    print(f"[{datetime.now()}] Monitoring target accounts...")

    for account in TARGET_ACCOUNTS:
        try:
            # Get user ID
            user = client.get_user(username=account.replace("@", ""))

            if user.data:
                # Get recent tweets from this account
                tweets = client.get_users_tweets(
                    id=user.data.id,
                    max_results=5,
                    tweet_fields=["author_id", "created_at", "public_metrics"]
                )

                if tweets.data:
                    for tweet in tweets.data:
                        # Check if tweet is about thumbnails
                        if any(kw.lower() in (tweet.text or "").lower() for kw in KEYWORDS):
                            print(f"\n✅ Relevant tweet from {account}:")
                            print(f"{tweet.text[:100]}...")
                            print(f"URL: https://twitter.com/i/status/{tweet.id}")
                            print("-" * 50)

        except Exception as e:
            print(f"Error monitoring {account}: {e}")

    print(f"[{datetime.now()}] Account monitoring complete.\n")

def post_daily_tip():
    """Post a daily thumbnail tip"""
    tips = [
        "📊 Thumbnail Tip #1:\n\n70% of YouTube views are on mobile.\n\nIf your thumbnail text isn't readable on a phone screen, it's not big enough.\n\nDesign for small screens first! 📱",

        "🎨 Thumbnail Tip #2:\n\nThe best thumbnail colors for CTR:\n• Red (urgency, excitement)\n• Yellow (attention-grabbing)\n• High contrast combinations\n\nTest what works for YOUR audience!",

        "😮 Thumbnail Tip #3:\n\nFaces drive clicks. Specifically:\n• Shocked/surprised expressions\n• Looking at the camera\n• Multiple faces = more curiosity\n\nBut make it authentic to your brand!",

        "📝 Thumbnail Tip #4:\n\nText overlay formula:\n\n3-5 words MAX\nBold, thick fonts\nContrasting color from background\nPosition: top or bottom third\n\nDon't let text cover faces!",

        "🧪 Thumbnail Tip #5:\n\nA/B test your thumbnails!\n\nCreate 3-5 variations:\n• Different expressions\n• Different text\n• Different colors\n\nUpload, wait 24hrs, keep the winner. 🏆",

        "💰 Thumbnail Tip #6:\n\nHuman designers: $30-100/thumbnail\nAI tools: ~$0.01/thumbnail\n\nFor A/B testing 10 variations per video, the math is clear.\n\nInvest saved money into better equipment/content!",

        "⏰ Thumbnail Tip #7:\n\nTime spent on thumbnails:\n• Pros: 30-45 min each\n• AI tools: 60 seconds\n\nThat's 45x faster. What could you do with an extra 5 hours per video?",

        "🎯 Thumbnail Tip #8:\n\nMrBeast's thumbnail formula:\n\n1. Clear subject (usually his face)\n2. Bright, saturated colors\n3. Simple composition\n4. One clear emotion/action\n\nSimple > Complex for CTR!",
    ]

    try:
        tip = tips[datetime.now().day % len(tips)]

        # For now, just log - uncomment to enable auto-post
        # response = client.create_tweet(text=tip)
        # print(f"✅ Posted tip: {tip[:50]}...")

        print(f"📝 Today's tip:\n{tip}")
        print("-" * 50)

    except Exception as e:
        print(f"Error posting tip: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("ThumbnailAI Twitter Monitor Bot")
    print("=" * 60)
    print(f"Monitoring {len(KEYWORDS)} keywords and {len(TARGET_ACCOUNTS)} accounts")
    print("Running in LOG-ONLY mode (no auto-replies/posts)")
    print("=" * 60)
    print()

    # Run immediately
    monitor_keywords()
    monitor_accounts()
    post_daily_tip()

    # Then schedule regular checks
    schedule.every(1).hours.do(monitor_keywords)
    schedule.every(4).hours.do(monitor_accounts)
    schedule.every().day.at("09:00").do(post_daily_tip)

    print("Bot running. Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)
