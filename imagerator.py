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
import sys
import time
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

def run(conf, r, i):
    print "# Imagerator running #"
    p, e, s = 0, 0, 0
    sym = '\\'
    sym = updateCLI(sym,p,e,s)
    mostRecent = None

    while True:
        processed = 0

        # get the sub
        subreddit = r.get_subreddit('A858DE45F56D9BC9')

        # if we've just started let's start from the begining, otherwise we'll pick up where we left off
        if mostRecent == None:
            subs = subreddit.get_new(limit=conf['block'])
        else:
            latest = "t3_{}".format(mostRecent)
            subs = subreddit.get_new(limit=conf['block'], params={'after': latest})

        # churn through the submissions
        for submission in subs:
            try:
                # make sure it's not in already_done
                if r.haventReplied(submission):
                    # get the text
                    text = r.getSubText(submission)
                    # make it into an image
                    try:
                        # try to turn it into an image
                        i.makeImg(text)
                    except:
                        # if we fail, skip it
                        db_interface.addSub(submission.id)
                        p += 1
                        pass
                    while True:
                        try:
                            # upload it
                            imgLink = i.uploadImage(submission.id)
                            try:
                                # post it
                                r.postComment(submission, imgLink)
                            except:
                                # start from the top and go again
                                mostRecent = None
                            break
                        except:
                            e += 1
                            sym = updateCLI(sym,p,e,s)
                            time.sleep(5)
                            pass
                    p += 1
                else:
                    s += 1
                    if s > p:
                        mostRecent = None
            except:
                e += 1
                pass

        updateCLI(sym,p,e,s)

    print "\r\nDone"
    return True

def updateCLI(loading, passed, error, skipped):
    # loading symbol dict
    loadDict = {
            '|': '/',
            '/': '-',
            '-': '\\',
            '\\': '|',
          }
    # standard message
    sys.stdout.write("\r{0} submissions processed: {1}".format(loadDict[loading],passed))

    # if there are errors lets put that on the cli too
    if error > 0:
        sys.stdout.write(", errors: {}".format(error))

    # if we skipped some for whatever reason lets detail that
    if skipped > 0:
        sys.stdout.write(", skipped: {}".format(skipped))

    # now push it all out to the cli
    sys.stdout.flush()

    # return the loading symbol we got to
    return loadDict[loading]


run(conf, r, i)