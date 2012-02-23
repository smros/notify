"""A handle for updating the database."""
from ConfigParser import RawConfigParser
import os.path
import sys
import datetime
sys.path.append('../../')
sys.path.append('/home/steve/notify/src/db')
import api
print sys.path
from projectStory import projectStoriesDB


## Config stuff here

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..','..','..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
DB_NAME =  os.path.join(
    os.path.dirname(__file__), '..','..','db',CONFIG.get('db', 'dbname') )

users=dict()
users['RI']='Rainer Iraschko'
users['SM']='Stephen Mroszczak'
users['DA']='Don Annett'
users['JC']='Johnny Cordova'
users['BF']='Bill Friedrich'

class dbHandler():
    
    def __init__(self,interested_in, getrecipients):
        self.interested_in = interested_in
        self.getrecipients = getrecipients
        
    def handle(self, message):

        print message
        prjID=message.project_id
        storyID=message.story_id
        owner=message.owner
        status=message.phase_name

        # Check all this logic, first check if status is the phase.
        # if working then enter new entry with owner and time
        # If not, check if it is in the dB with startTime, but no endTime. This
        # should indicate time event that needs to be logged.
        #
        # Remember this handler gets called for both moved to working and moved out.
        # and maybe for everything
        #
        # Or watch only from .? to Working or from ?.to Working
        #
        # Check if story is in DB yet, with startTime
        print 'DB NAME'
        print DB_NAME
        db=projectStoriesDB(DB_NAME)

        data=db.getStories(prjID, storyID)
        print 'Here is the current data in the DB re: this story'
        print data
        print 'Status: ' + status
        print '---------'
        if status =='Working':
            if data.__len__()==0:
                print 'No data'
                print 'Inserting new tracking event into db'
                db.insertEvent(message)
            else:
                foundOpen=False
                for item in data:
                    print 'Story exists in db, looking for open entry...'
                    print item
                    print '-----'
                   # Check for open entry (i.e. one with no endTime)
                    if item[1]==None:
                        foundOpen=True
                        # Found an open entry against this story, check if owner
                        # changed
                        if item[2] != owner:
                            print 'Owner changed!'
                            # Close old entry
                            db.updateEndTime(prjID, storyID, item[2], item[0], datetime.datetime.now().isoformat('-'))
                            # Insert new one
                            db.insertEvent(message)

                        else:
                            # Ignore, something else triggered the event,
                            # Owner is the same, status is still working so ignore
                            pass

                if not(foundOpen):
                    # An open entry was not found, create a new one
                    print 'Does not exist, creating new event..'
                    db.insertEvent(message)


        else:
            # Status is 'not' working, check to see if this is in the db
            # without an endtime.
            for item in data:
                    #
                    # Check for open entry (i.e. one with no endTime) if we go
                    # through all entries with no updates, then the story
                    # probably moved from a !Working status to another !Working
                    # status, so no action required.
                    #
                    if item[1]==None:
                        # Found our entry, update with endtime.
                        db.updateEndTime(prjID, storyID, owner, item[0], datetime.datetime.now().isoformat('-'))

        # Check for unlogged "timecard comments".  This should be in different handler
        # or triggered only when a comment event happens, but for now, check on every
        # story.

        # Get the story here, put in item
        #
        # Then scan comments.
        #
        print 'Entering comments scan, looking for unlogged timecard messages.'
        item = api.get_story(prjID, storyID)

        for comments in item['comments']:

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
                timeCardOwner=users[owner]
                if parsedComment[-1].lstrip()=='Logged':
                    print 'Comment already logged!'
                else:
                    print 'New Entry found'
                    print 'Need to log ' + str(duration) + ' hours for ' + timeCardOwner
                    #
                    # Now update comment with logged, as if it was updated in the db
                    #
                    updateText='TC:'+ owner + ', ' + duration +', '+ 'Logged'
                    api.update_comment(prjID, storyID, id, updateText)
                    #
                    # And, update the database with a timecard entry.
                    #
                    db.insertTimecard(message, timeCardOwner, duration)


        db.closeDB()


            # If so, check if story has been moved to anything but Working,
            # then  calculate duration, update endtime

        # Else, if story is not in db, check if it is marked working
            # If so, insert a new event into DB.
            # If not, ignore quit


  




        
