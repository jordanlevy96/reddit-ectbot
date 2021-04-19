import praw
import re
from collections import deque

reddit = praw.Reddit('DEFAULT', config_interpolation='basic')
subreddit = reddit.subreddit('all')

ect_regex = '\W[Ee]ct\W'
cache = deque(maxlen=200) # maintain a cache to avoid duplicating effort

running = True
while running:
   comments = subreddit.comments(limit=None)
   for comment in comments:
      if comment.id in cache:
         break
      cache.append(comment.id)

      if re.search(ect_regex, comment.body):
         try:
            print(comment.body)
            print(comment.permalink)
            print('---------------------')
            # do stuff

         except Exception as e:
            print("ERROR: ", e, file=sys.stderr)
