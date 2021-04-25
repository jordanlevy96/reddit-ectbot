# ECT Bot

## Overview

A reddit bot that (politely) corrects people who write "ect" instead of "etc" in comments. Like many other reddit bots, this relies on PRAW, the Python Reddit API Wrapper.

I parse through /r/all's comments using PRAW.Subreddit.comments, check them against a regex for the dreaded "ect," and attempt to educate them about their mistake in a response comment.

## Acknowledgements

[Reddit](www.reddit.com) is of course the source of all of the content.

[PRAW](https://github.com/praw-dev/praw), mentioned above, is a critical Python package that makes this all doable.

GitHub user dmarx created [a valuable example of a reddit bot](https://gist.github.com/dmarx/5550922) that this is loosely based on.

The [Python For Engineers](https://www.pythonforengineers.com/build-a-reddit-bot-part-1/) Reddit bot tutorial was also a good resource for learning how to write this (and is more up-to-date than the example above).

## TODOs
- remove unused environment files from figuring out deployment
- send myself an email if ectbot goes down
