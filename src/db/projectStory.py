#! /usr/bin/python

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="steve"
__date__ ="$16-Feb-2012 10:42:38 AM$"

from sqllite import sqlliteDB
import datetime

class projectStoriesDB(sqlliteDB):

    def createProjectStoriesDB(self):
        tableInit="""

            drop table if exists quotes;

            create table projectStories(
                project TEXT,
                story TEXT,
                owner TEXT,
                startTime DATETIME,
                endTime DATETIME,
                duration FLOAT,
                comment TEXT,
                timecard INTEGER,
                primary key (project, story, owner, startTime)
                );

            create index idx1 on projectStories(
                project,
                story,
                owner,
                startTime
                );

            """

        self.executeScript(tableInit)
        self.closeDB()

    def insertEvent(self, message):
        # Build the sql trasaction here and run the insert
        prefix = ''' insert or ignore into projectStories (project, story, owner, startTime) values (?,?,?,?)'''
        dataTuple=(message.project_id,
        message.story_id,
        message.owner,
        datetime.datetime.now().isoformat('-')
        )

#        print prefix
#        print dataTuple

        self.executeTransaction2(prefix, dataTuple)

    def insertTimecard(self, message, timeCardOwner, duration):
    # Build the sql trasaction here and run the insert
        prefix = ''' insert or ignore into projectStories (project, story, owner, startTime, duration, timecard) values (?,?,?,?,?,?)'''
        dataTuple=(message.project_id,
        message.story_id,
        timeCardOwner,
        datetime.datetime.now().isoformat('-'),
        str(duration),
        '1'

        )

        #        print prefix
        #        print dataTuple

        self.executeTransaction2(prefix, dataTuple)

    def getStories(self, projectID=None, storyID=None, owner=None):
        prefix = ''' select startTime, endTime, owner from projectStories where project = ? and story = ?'''
        data=self.executeQueryFetchAll2(prefix, (projectID, storyID ) )
        return(data)

    def updateEndTime(self, projectID=None, storyID=None, owner=None, startTime=None, endTime=None):
        prefix = ''' update projectStories set endTime = ? where project = ? and story = ? and owner = ? and startTime = ?  '''
        data=self.executeTransaction2(prefix, (endTime, projectID, storyID, owner, startTime ) )
        

    def getEndTime(self, projectID=None, storyID=None, owner=None, startTime=None):
        prefix = ''' select endTime from projectStories where project = ? and story = ? and owner = ? and startTime = ? '''
        data=self.executeQueryFetchAll2(prefix, (projectID, storyID, owner, startTime ) )
        return(data)

#    def getTitlesFromDB(self):
#        prefix = ''' select distinct title from quotes'''
#        data=self.executeQueryFetchAll(prefix)
#        return(data)



if __name__ == "__main__":

    q=projectStoriesDB('agileZenStories.db')
    #q.createProjectStoriesDB()
    data=q.getEndTime('12345', '1', 'steve','2008-01-01-12:00:00')
    print data
    if data.__len__()==0:
        print 'No data'
    else:
        print data[0]
    data=q.getEndTime('99999', '3', 'johnny','1999-01-01-12:00:00')
    if data.__len__()==0:
        print 'No data'
    else:
        print data[0]
    data=q.getEndTime('99999', '3', 'johnny','1999-01-01-12:01:00')
    if data.__len__()==0:
        print 'No data'
    else:
        print data[0]

    data=q.getStories('99999', '3','ALL')
    if data.__len__()==0:
        print 'No data'
    else:
        print 'Found data!'
        print data

        for item in data:
            if item[1]==None:
                print 'Found an open entry'
                print item[0]
            else:
                print 'Found a closed entry:'
                print item[0]
                print item[1]
                print item[2]


    q.closeDB()


    #q.createQuotesDB()

