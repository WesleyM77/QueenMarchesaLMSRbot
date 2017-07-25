import praw
import pdb
import re
import os
import time

reddit = praw.Reddit('bot1')
subreddit = reddit.subreddit("magictcg+edh+pythonforengineers")

lmsrcomment = """>Queen Marchesa (long may she reign)\n
                    \nFTFY. I'm a bot. If I've made a mistake, click [here.]
                    (https://www.reddit.com/message/compose?to=shadowwesley77)
                    """
        
if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []
else:
    with open("posts_replied_to.txt", "r") as f:
       posts_replied_to = f.read()
       posts_replied_to = posts_replied_to.split("\n")
       posts_replied_to = list(filter(None, posts_replied_to))

if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []
else:
    with open("comments_replied_to.txt", "r") as t:
       comments_replied_to = t.read()
       comments_replied_to = comments_replied_to.split("\n")
       comments_replied_to = list(filter(None, comments_replied_to))

checked = 0

#Check submission titles
for submission in subreddit.stream.submissions():
    if submission.id not in posts_replied_to:
        checked = checked + 1
        if checked % 100 == 100:
            print ("Checked ", checked ," posts")
        if re.search("Queen Marchesa", submission.title, re.IGNORECASE) and not re.search("long may she reign", submission.title, re.IGNORECASE):
            submission.reply(lmsrcomment)
            print("Bot replied to: ", submission.title)
            posts_replied_to.append(submission.id)
            with open("posts_replied_to.txt", "w") as f:
                for post_id in posts_replied_to:
                    f.write(post_id + "\n")
        #Check comments of post
        submission.comments.replace_more(limit=0)
        comments = submission.comments[:]
        while comments:
            comment = comments.pop(0)
            if comment.id not in comments_replied_to and comment.author is not "MTGCardFetcher":
                if re.search("Queen Marchesa", comment.body, re.IGNORECASE) and not re.search("long may she reign", comment.body, re.IGNORECASE):
                    comment.reply(lmsrcomment)
                    print("Bot replied to comment under: ", submission.title)
                    comments_replied_to.append(comment.id)
                    with open("comments_replied_to.txt", "w") as t:
                        for post_id in comments_replied_to:
                            t.write(post_id + "\n")
                comments.extend(comment.replies)






            
            
