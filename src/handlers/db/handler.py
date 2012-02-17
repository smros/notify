"""A handle for updating the database."""
from ConfigParser import RawConfigParser
import os.path
import sys
sys.path.append('../../src')
sys.path.append('../../src/db')
from projectStory import projectStoriesDB
import api

## Config stuff here

# load config
CFG_PATH = os.path.join(
    os.path.dirname(__file__), '..','..','..', 'notify.cfg')
CONFIG = RawConfigParser()
CONFIG.read(CFG_PATH)
DB_NAME =  os.path.join(
    os.path.dirname(__file__), '..','..','..',CONFIG.get('db', 'dbname') )


class dbHandler():
    
    def __init__(self,interested_in, getrecipients):
        self.interested_in = interested_in
        self.getrecipients = getrecipients
        
    def handle(self, message):

        print message
        prjID=message.project_id
        storyID=message.story_id
        owner=message.owner
        status=message.status

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

        db=projectStoriesDB(DB_NAME)

        data=db.getStories(prjID, storyID, owner)
        print data
        if data.__len__()==0:
            print 'No data'
            db.insertEvent(message)
        else:
            for item in data:
                # Now look for a endTIme.  If it exists, skip
                # that item.
                if item[1]==None:
                    # Found our entry, update with endtime.
                    db.updateEndTime(prjID, storyID, owner, item[0])
            # No endtime was found, item must be new
            db.insertEvent(message)

        db.closeDB()


            # If so, check if story has been moved to anything but Working,
            # then  calculate duration, update endtime

        # Else, if story is not in db, check if it is marked working
            # If so, insert a new event into DB.
            # If not, ignore quit


  




        
