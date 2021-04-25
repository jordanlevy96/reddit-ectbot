import praw
import re
import sys
import os
import time
import subprocess

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
seconds_in_hour = 3600

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
   parent = comment.parent()
   if comment.score < 0:
      print('Deleting comment', comment.id, 'due to low score.')
      comment.delete()
   elif parent.author is not None and commenter_requested_delete(comment, parent.author.name):
      print('Deleting comment', comment.id, 'due to commenter request.')
      comment.delete()

def commenter_requested_delete(comment, commenter):
   for reply in comment.replies:
      if reply.author.name == commenter:
         if "!delete" in reply.body.lower():
            return True

   return False

def ectbot(reddit, bot):
   subreddit = reddit.subreddit(sub)
   last_history_check = time.time()
   proc = None

   print('Starting up ectbot...')

   running = True
   while running:
      print('Creating comment stream...')
      comments = subreddit.stream.comments(skip_existing=True)
      try: 
         for comment in comments:
            if comment.author is None:
               # ignore comments from deleted users
               continue

            if comment.author.name == 'ectbot':
               # ignore comments made from self
               print('~~~~~~~~~~~~~~~~')
               print('Found ectbot comment at http://www.reddit.com' + comment.permalink)
               print('~~~~~~~~~~~~~~~~')

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
                  print('Ect corrected!')
                  ectcomments += 1

            # trigger a history check every hour
            current_time = time.time()
            if proc is None or (current_time >= last_history_check + seconds_in_hour and proc.poll() is not None):
               last_history_check = current_time
               print('Forking process to check history...')
               proc = subprocess.Popen(['python', 'ectbot.py', '--check-history'])
               print('Forked process started!')

      except KeyboardInterrupt:
         print('Program stopped by user. Exiting...')
         running = False
      except praw.exceptions.APIException as e:
         print('[ERROR]:', e, file=sys.stderr)
         print('Sleeping 30 sec...', file=sys.stderr)
         time.sleep(30)       
      except Exception as e:
         print('[ERROR]: ', e, file=sys.stderr)
         running = False

def check_history(reddit, bot):
   count = 0
   old_comments = bot.comments.new(limit=None)
   for comment in old_comments:
      handle_own_comment(comment)
      count += 1
   print('Checked all', count, 'old ectbot comments')

def main():
   reddit = init()
   bot = reddit.redditor('ectbot')

   if len(sys.argv) > 1:
      arg = sys.argv[1]
      print('ectbot started with option:', arg)
      if arg != '--check-history':
         print('Anamalous arg found:', arg, file=sys.stderr)
         sys.exit(2)
      else:
         print('Checking ectbot history...')
         check_history(reddit, bot)
   else:
      ectbot(reddit, bot)

if __name__ == '__main__':
   main()
