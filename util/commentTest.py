#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

import os.path
from ConfigParser import RawConfigParser
import sys
sys.path.append('../src')
import api
import time
#import yaml

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
WATCHER_PATH = os.path.join(
    os.path.dirname(__file__), '..',CONFIG.get('watcher', 'path') )
API_KEY = CONFIG.get('api','key')

if __name__ == "__main__":

#    zz=raw_input('This will overwrite any existing watcher files.  Proceed? (Y/N)?')
#    if zz!='Y' and zz!='y':
#        sys.exit(0)
    print API_KEY
    print CFG_PATH
    print WATCHER_PATH

    # Test parameters

#    projID=35644
#    storyID=3


#    print 'Testing add comment'
#    storyInit=api.get_story(projID, storyID)
#    print storyInit

#    commentTxt='Test Comment from API'
#
#    resp=api.add_comment(projID, storyID, commentTxt)
#    print resp
##
#    projID=32199
#    storyID=5
#    print 'Getting story ' + str(storyID)
#    print api.get_story(projID, storyID)
#
#    commentID=343796
#    commentTxt = 'Test of update comment: ' + str(time.time())
#
#    print 'Testing update comment'
#    resp=api.update_comment(projID, storyID, commentID, commentTxt)

# Test search for unlogged time comments, will have te

    # Import users from yaml file.  Then load all stories from a project
    # cycle through all comments looking for lines that begin with TC:
    #
    #Examples:
    #
    #TC: 4.5, SM, Worked on plane, Logged
    #TC: -4.5, SM, Correction
    #TC: 5.0, RI, Worked on weekend
    #
    # Get this from yaml file later
    users=dict()
    users['RI']='iraschko'
    users['SM']='smroszczak'
    users['DA']='dannet'
    users['JC']='jcordova'

    # Get stories
    projID=35644

    stories=api.get_stories(projID)

    print 'All stories..'
    print stories['items']

    print 'Now printing comments..'
    
    for item in stories['items']:
        for comments in item['comments']:
            storyID=item['id']
            print 'Comment ID: ' + str(comments['id']) + ' comment text: ' + comments['text']
            id=comments['id']
            cText=comments['text']
            stripHeader=cText.split(':')
            print 'stripHeader'
            print stripHeader[0]
            if stripHeader.__len__()>1:
                print stripHeader[1]
                print str(stripHeader[1]).split(',')
            if stripHeader[0]=='TC':
                print 'Found log entry'
                parsedComment=str(stripHeader[1])
                print 'parsed Comment:'
                parsedComment=parsedComment.split(',')

                duration=parsedComment[1].lstrip()
                owner=parsedComment[0].lstrip()
                if parsedComment[-1].lstrip()=='Logged':
                    print 'Comment already logged!'
                else:
                    print 'New Entry found'
                    print 'Need to log ' + str(duration) + ' hours for ' + users[owner]
                    #
                    # Now update comment with logged, as if it was updated in the db
                    #
                    updateText='TC:'+ owner + ', ' + duration +', '+ 'Logged'
                    api.update_comment(projID, storyID, id, updateText)
                    

