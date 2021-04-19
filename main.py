import praw
import re
import sys
from collections import deque
from time import sleep

message = """
"Ect" is a common misspelling of "etc," an abbreviated form of the Latin phrase "et cetera." Other abbreviated forms are **etc.**, **&c.**, **&c**, and **et cet.** The Latin translates as "et" to "and" + "cetera" to "the rest;" a literal translation to "and the rest" is the easiest way to remember how to use the phrase. 

[Check out the wikipedia entry if you want to learn more.](https://en.wikipedia.org/wiki/Et_cetera)

^(I am a bot, and this action was performed automatically.)
"""
ect_regex = '\W[Ee]ct(?:\W|$)'
etc_regex = '\W[Ee]tc(?:\W|$)'
sub = 'pythonforengineers'
cache = deque(maxlen=200) # maintain a cache to avoid duplicating effort

reddit = praw.Reddit('DEFAULT', config_interpolation='basic')
subreddit = reddit.subreddit(sub)
bot = reddit.redditor('ectbot')

count = 0

running = True
while running:
   comments = subreddit.comments(limit=None)
   try: 
      for comment in comments:
         if comment.id in cache:
            break
         cache.append(comment.id)

         if comment.author.name == 'ectbot':
            print('Hi, self!')
            continue

         # if comment.body is message:
         #    print('Found self!')
         #    continue

         if re.search(ect_regex, comment.body) and not re.search(etc_regex, comment.body):
               print(comment.body)
               print('http://www.reddit.com' + comment.permalink)
               print('---------------------')
               
               comment.reply(message)

   except KeyboardInterrupt:
      print('Program stopped by user. Exiting...')
      running = False
   except praw.errors.APIException as e:
      print('[ERROR]:', e, file=sys.stderr)
      print('sleeping 30 sec', file=sys.stderr)
      sleep(30)       
   except Exception as e:
      print('ERROR: ', e, file=sys.stderr)
      print('Swallowing error!', file=sys.stderr)
      running = False
