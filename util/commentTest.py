#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

import os.path
from ConfigParser import RawConfigParser
import sys
sys.path.append('../src')
import api
import time

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

    projID=35644
    storyID=3


    print 'Testing add comment'
    storyInit=api.get_story(projID, storyID)
    print storyInit

#    commentTxt='Test Comment from API'
#
#    resp=api.add_comment(projID, storyID, commentTxt)
#    print resp
##
#    projID=32199
#    storyID=5
    print 'Getting story ' + str(storyID)
    print api.get_story(projID, storyID)

    commentID=343796
    commentTxt = 'Test of update comment: ' + str(time.time())

    print 'Testing update comment'
    resp=api.update_comment(projID, storyID, commentID, commentTxt)


