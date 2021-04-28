# ECTBOT Release Notes

[Source](https://github.com/jordanlevy96/reddit-ectbot)

### 28 April 2021 - v1.3.2
- fix for replies from deleted accounts

### 26 April 2021 - v1.3.1
- ignore inappropriate subreddits (e.g. /r/depression)
- comment.refresh() must be called to view replies -> !delete requests should work now

### 25 April 2021 - v1.3.0
- fork a process to check ectbot history once per hour

### 25 April 2021 - v1.2.1
- use lower() to handle more !delete calls
- handle ectbot comments with deleted parents

### 25 April 2021 - v1.2.0
- added deletion functionality
- replaced cache with stream to handle double commenting

### 24 April 2021 - v1.1.0
- add login option using environment variables
- fix praw exception handling
- handle banned subreddits

### 23 April 2021 - v1.0.0
- properly set up build requirements

### 19 April 2021 - v0.1.0
- initial release
