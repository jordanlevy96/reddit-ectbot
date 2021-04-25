import praw
import re
import sys
import os
from collections import deque
from time import sleep

message = """
Hello! You have made the mistake of writing "ect" instead of "etc!"

"Ect" is a common misspelling of "etc," an abbreviated form of the Latin phrase "et cetera." Other abbreviated forms are **etc.**, **&c.**, **&c**, and **et cet.** The Latin translates as "et" to "and" + "cetera" to "the rest;" a literal translation to "and the rest" is the easiest way to remember how to use the phrase. 

[Check out the wikipedia entry if you want to learn more.](https://en.wikipedia.org/wiki/Et_cetera)

^(I am a bot, and this action was performed automatically. Comments with a score less than zero will be automatically removed. If I commented on your post and you don't like it, reply with "!delete" and I will remove the post, regardless of score. Message me for bug reports.)
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

   print('Successfully signed in!')
   return reddit

def handle_own_comment(comment):
   commenter = comment.parent().author.name
   if comment.score < 0:
      print('Deleting comment', comment.id, 'due to low score.')
      comment.delete()
   elif commenter_requested_delete(comment, commenter):
      print('Deleting comment', comment.id, 'due to commenter request.')
      comment.delete()

def commenter_requested_delete(comment, commenter):
   for reply in comment.replies:
      if reply.author.name == commenter:
         if "!delete" in reply.body:
            return True

   return False

def ectbot(reddit):
   subreddit = reddit.subreddit(sub)
   bot = reddit.redditor('ectbot')
   ectcomments = 0

   print('Starting up ectbot...')

   running = True
   while running:

      if (ectcomments >= 90):
         print('Checking last 100 ectbot posts...')
         last50 = bot.comments.new(limit=100)
         for c in last50:
            handle_own_comment(c)
         ectcomments = 0

      print('Viewing more comments...')

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
               # ignore comments made from self
               print('Found ectbot comment at http://www.reddit.com' + comment.permalink)

               handle_own_comment(comment)

               continue

            if re.search(ect_regex, comment.body) and not re.search(etc_regex, comment.body):
                  print('---------------------')
                  print('Found an "etc" by ' + comment.author.name + ', who said:')
                  print(comment.body)
                  print('http://www.reddit.com' + comment.permalink)
                  print('---------------------')

                  if reddit.subreddit(comment.subreddit.display_name).user_is_banned:
                     # ignore comments in banned subreddits
                     print('ectbot is banned from', comment.subreddit.display_name)
                     continue
                  
                  comment.reply(message)
                  ectcomments += 1

      except KeyboardInterrupt:
         print('Program stopped by user. Exiting...')
         running = False
      except praw.exceptions.APIException as e:
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
