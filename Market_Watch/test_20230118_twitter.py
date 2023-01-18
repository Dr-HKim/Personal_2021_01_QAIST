import json
import twitter
from collections import Counter

CONSUMER_KEY = "rr1FZWHkV96tsJNVUyz3yaQxM"
CONSUMER_SECRET = "j0Vy7ahfOrVnLQbuDu0OvmIaRkv8lsocvUsJzP1CYH70F5JdeL"
ACCESS_TOKEN = "141858321-C4jSlIgSGA5Rj57P0mvxcp8aZ5gUFjK9P9laOlou"
ACCESS_SECRET = "rAteSAKY3NCqAuMm4JOrYDHqCHIU4UPkshG5x0h0RjB2Y"

twitter_api = twitter.Api(consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET)

# JTBC 뉴스 트윗 분석
account = "@JTBC_news"
statuses = twitter_api.GetUserTimeline(screen_name=account, count=2000, include_rts=True, exclude_replies=False)
result = []
for status in statuses:
    for word in status.text.split(" "):
        result.append(word)
Counter(result).most_common(100)

# 코로나 키워드가 포함된 tweet 수집
query = ["코로나"]
output_file_name = "stream_result.txt"

with open(output_file_name, "w", encoding="utf-8") as output_file:
    stream = twitter_api.GetStreamFilter(track=query)
    while True:
        for tweets in stream:
            tweet = json.dumps(tweets, ensure_ascii=False)
            print(tweet, file=output_file, flush=True)


