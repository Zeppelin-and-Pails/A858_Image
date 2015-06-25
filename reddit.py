"""
reddit

A package for getting content off reddit, and sometimes putting it there

@category   silly
@version    $ID: 1.1.1, 2015-02-19 17:00:00 CST $;
@author     KMR, Jason
@licence    GNU GPL v.3
"""
import praw
import db_interface

class reddit:
    rAPI = None
    post = None

    def __init__(self, conf):
        user_agent = ("A858 Imagerator")
        self.rAPI = praw.Reddit(user_agent=user_agent)
        self.rAPI.login(username=conf['u'], password=conf['p'])

    def get_subreddit(self, sub):
        return self.rAPI.get_subreddit(sub)

    def haventReplied(self, sub):
        if db_interface.getSub( sub.id ) is None:
            return True
        return False

    def getSubText(self, sub):
        return sub.selftext

    def postComment(self, sub, imgLink):
        sub.add_comment("{}\n\n I am A8582Image, I make images.".format(imgLink))
        db_interface.addSub(sub.id)