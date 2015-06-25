#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
imagerator

makes images from A858 posts, uploads them, and links them to the post

@category   silly
@version    $ID: 1.1.1, 2015-02-19 17:00:00 CST $;
@author     KMR, Jason
@licence    GNU GPL v.3
"""
import os
import yaml
import imgur
import reddit
import db_interface

#Work out where we are
DIR = os.path.dirname(os.path.realpath(__file__))
#Get the config
conf = yaml.safe_load(open("{}/A858_image.cfg".format(DIR)))

r = reddit.reddit(conf)
i = imgur.imgur(conf)

def run():
    # get the sub
    subreddit = r.get_subreddit('A858DE45F56D9BC9')
    # churn through the submissions
    mostRecent = db_interface.getMostRecent()
    subs = None
    if mostRecent == None:
        subs = subreddit.get_new(limit=conf['block'])
    else:
        latest = "t3_{}".format(mostRecent)

        subs = subreddit.get_new(limit=conf['block'], params={'after': latest})

    for submission in subs:
        # make sure it's not in already_done
        if r.haventReplied(submission):
            # get the text
            text = r.getSubText(submission)
            # make it into an image
            i.makeImg(text)
            imgLink = i.uploadImage(submission.id)
        # post it
            r.postComment(submission, imgLink)

# loops as far as the eye can see
while True:
    run()
