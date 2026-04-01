#!/usr/bin/env python3
"""
ThumbnailAI Reddit Monitor Bot
Monitors subreddits for thumbnail-related questions and auto-replies with helpful tips
"""

import praw
import schedule
import time
import os
from datetime import datetime

# Reddit API credentials (get at https://www.reddit.com/prefs/apps)
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="thumbnailai_helper/1.0 by u/YourRedditUsername",
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# Subreddits to monitor
SUBREDDITS = [
    "NewTubers",
    "PartneredYoutube",
    "SmallYTChannel",
    "ContentCreators",
    "VideoEditing",
    "youtube",
    "vlogging"
]

# Keywords to monitor
KEYWORDS = [
    "thumbnail",
    "thumbnail designer",
    "thumbnail maker",
    "thumbnail help",
    "thumbnail art",
    "youtube thumbnail",
    "ctr help",
    "click through rate"
]

# Helpful reply template (not spammy!)
REPLY_TEMPLATE = """
Great question about thumbnails! They're crucial for CTR.

A few quick tips:
1. **High contrast** - Make sure text pops against the background
2. **Faces sell** - Expressive faces get more clicks (shock, excitement, surprise)
3. **Text overlay** - 3-5 words max, large and readable on mobile
4. **A/B test** - Try multiple versions to see what works

I actually built a free tool that generates thumbnails in ~60 seconds using AI if you want to try it: **[ThumbnailAI](https://thumbnailai.app)** - no affiliation, just found it useful.

Good luck with your channel! 🚀
"""

def is_valid_post(post):
    """Filter out posts we shouldn't comment on"""
    # Skip if post is locked or archived
    if post.locked or post.archived:
        return False

    # Skip if post is older than 7 days
    post_age = datetime.now() - datetime.fromtimestamp(post.created_utc)
    if post_age.days > 7:
        return False

    # Skip if we already commented
    for comment in post.comments:
        if comment.author and comment.author.name == reddit.user.me().name:
            return False

    return True

def find_and_reply():
    """Monitor subreddits and reply to relevant posts"""
    print(f"[{datetime.now()}] Starting monitoring cycle...")

    for subreddit_name in SUBREDDITS:
        try:
            subreddit = reddit.subreddit(subreddit_name)

            # Get new posts
            for submission in subreddit.new(limit=50):
                # Check if post matches keywords
                title_match = any(keyword.lower() in submission.title.lower() for keyword in KEYWORDS)
                selftext_match = any(keyword.lower() in (submission.selftext or "").lower() for keyword in KEYWORDS)

                if title_match or selftext_match:
                    if is_valid_post(submission):
                        print(f"\n✅ Found relevant post: {submission.title}")
                        print(f"URL: https://reddit.com{submission.permalink}")

                        # For now, just log - uncomment to enable auto-reply
                        # try:
                        #     submission.reply(REPLY_TEMPLATE)
                        #     print("✅ Replied successfully!")
                        # except Exception as e:
                        #     print(f"❌ Reply failed: {e}")

                        print("-" * 50)

        except Exception as e:
            print(f"Error in r/{subreddit_name}: {e}")

    print(f"[{datetime.now()}] Cycle complete.\n")

def search_and_reply():
    """Search Reddit broadly for thumbnail discussions"""
    print(f"[{datetime.now()}] Starting search cycle...")

    for keyword in KEYWORDS:
        try:
            results = reddit.subreddit("all").search(keyword, sort="new", limit=20)

            for post in results:
                if post.subreddit_name in SUBREDDITS:
                    continue  # Already covered by subreddit monitoring

                if is_valid_post(post):
                    print(f"\n✅ Found via search: {post.title}")
                    print(f"URL: https://reddit.com{post.permalink}")
                    print(f"Subreddit: r/{post.subreddit_name}")
                    print("-" * 50)

        except Exception as e:
            print(f"Search error for '{keyword}': {e}")

    print(f"[{datetime.now()}] Search cycle complete.\n")

if __name__ == "__main__":
    print("=" * 60)
    print("ThumbnailAI Reddit Monitor Bot")
    print("=" * 60)
    print(f"Monitoring {len(SUBREDDITS)} subreddits for {len(KEYWORDS)} keywords")
    print("Running in LOG-ONLY mode (no auto-replies)")
    print("=" * 60)
    print()

    # Run immediately
    find_and_reply()
    search_and_reply()

    # Then schedule regular checks
    schedule.every(30).minutes.do(find_and_reply)
    schedule.every(2).hours.do(search_and_reply)

    print("Bot running. Press Ctrl+C to stop.\n")

    while True:
        schedule.run_pending()
        time.sleep(60)
