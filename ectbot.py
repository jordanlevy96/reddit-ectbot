import praw
import re
import sys
import os
from collections import deque
from time import sleep

message = """
"Ect" is a common misspelling of "etc," an abbreviated form of the Latin phrase "et cetera." Other abbreviated forms are **etc.**, **&c.**, **&c**, and **et cet.** The Latin translates as "et" to "and" + "cetera" to "the rest;" a literal translation to "and the rest" is the easiest way to remember how to use the phrase. 

[Check out the wikipedia entry if you want to learn more.](https://en.wikipedia.org/wiki/Et_cetera)

^(I am a bot, and this action was performed automatically.)
"""
ect_regex = '\W[Ee]ct(?:\W|$)'
etc_regex = '\W[Ee]tc(?:\W|$)'
sub = 'all'
botname = 'ectbot'
cache = deque(maxlen=200) # maintain a cache to avoid duplicating effort (note: this does not seem to help when restricted to a single subreddit
# I guess it loops around and starts viewing old comments again?)


def init():
   """ initialize app, creating reddit object
      uses praw.ini file if available, otherwise expects environment variables
   """

   reddit = None

   try:
      if os.path.exists('./praw.ini'):
         print('Starting up using praw.ini...')
         reddit = praw.Reddit('DEFAULT', config_interpolation='basic')
      else:
         print('Starting up using environment variables...')
         reddit_username = os.environ['reddit_username']
         reddit_password = os.environ['reddit_password']
         client_id = os.environ['client_id']
         client_secret = os.environ['client_secret']
         user_agent = os.environ['user_agent']
         reddit = praw.Reddit(username = reddit_username,
                password = reddit_password,
                client_id = client_id,
                client_secret = client_secret,
                user_agent = user_agent)

   except Exception as e:
      print('Failed to log in!', sys.stderr)
      print(e, sys.stderr)
      sys.exit(1)

   if not reddit:
         raise Exception('Failed to create Reddit object.')

   return reddit

def ectbot(reddit):
   subreddit = reddit.subreddit(sub)
   bot = reddit.redditor('ectbot')
   running = True
   while running:
      comments = subreddit.comments(limit=None)
      try: 
         for comment in comments:
            if comment.id in cache:
               break
            cache.append(comment.id)

            if comment.author is None:
               # ignore comments from deleted users
               continue

            if comment.author.name == 'ectbot':
               print('Found ectbot comment at http://www.reddit.com' + comment.permalink)
               continue

            if re.search(ect_regex, comment.body) and not re.search(etc_regex, comment.body):
                  print('---------------------')
                  print('Replying to ' + comment.author.name + ', who said:')
                  print(comment.body)
                  print('http://www.reddit.com' + comment.permalink)
                  print('---------------------')
                  
                  comment.reply(message)

      except KeyboardInterrupt:
         print('Program stopped by user. Exiting...')
         running = False
      except praw.errors.APIException as e:
         print('[ERROR]:', e, file=sys.stderr)
         print('Sleeping 30 sec...', file=sys.stderr)
         sleep(30)       
      except Exception as e:
         print('[ERROR]: ', e, file=sys.stderr)
         running = False

def main():
   reddit = init()
   ectbot(reddit)

if __name__ == '__main__':
   main()
