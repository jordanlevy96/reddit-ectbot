import praw
import re
from collections import deque

reddit = praw.Reddit('DEFAULT', config_interpolation='basic')
subreddit = reddit.subreddit('AskReddit')

ect_regex = '\Wect\W'

count = 0

cache = deque(maxlen=200)

running = True
while running:
   comments = subreddit.comments(limit=None)
   for comment in comments:
      if comment.id in cache:
         break
      cache.append(comment.id)

      print('Comments viewed: ', count)
      count += 1

      if re.search(ect_regex, comment.body, re.IGNORECASE):
         try:
            print(comment.body)
            # do stuff

         except Exception as e:
            print("ERROR: ", e, file=sys.stderr)
