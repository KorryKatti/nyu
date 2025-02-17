import feedparser
import random
import time
import socket

def get_headlines(feed_links):
    headlines = []
    max_headlines = 49 + random.randint(0, 10)  # Fetch 49 to 59 headlines per source
    skipped_feeds = []
    min_timeout = 5  # 5 seconds (optimal for quant systems, avoids too much wait time)
    socket.setdefaulttimeout(min_timeout)  # Set timeout for all connections

    for link in feed_links:
        retries = 3  # Try up to 3 times
        for attempt in range(retries):
            try:
                print(f"Fetching: {link} (Attempt {attempt + 1}/{retries})")
                start_time = time.time()  # Record time before fetching
                feed = feedparser.parse(link)
                elapsed_time = time.time() - start_time

                # If fetching takes longer than the minimum timeout, skip the feed
                if elapsed_time > min_timeout:
                    print(f"⏳ Took too long to fetch {link} ({elapsed_time:.2f}s), skipping...")
                    skipped_feeds.append(link)
                    break

                # Check if parsing actually got entries (avoid empty results)
                if not feed.entries:
                    raise Exception("Empty feed or parsing failed")

                for i in range(min(max_headlines, len(feed.entries))):
                    headlines.append(feed.entries[i].title)

                print(f"✅ Success: {link} ({len(feed.entries)} headlines)")

                break  # success, exit retry loop

            except Exception as e:
                print(f"❌ Error fetching {link}: {e}")
                if attempt < retries - 1:
                    print("🔄 Retrying in 3 seconds...")
                    time.sleep(3)
                else:
                    print(f"🚨 Skipping {link} after {retries} failed attempts.")
                    skipped_feeds.append(link)

    print("\n🚫 Skipped Feeds:", skipped_feeds)
    return headlines
