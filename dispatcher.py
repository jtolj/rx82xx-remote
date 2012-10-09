import logging
import sqlite3 as lite
import sys
import time
from apscheduler.scheduler import Scheduler
from apscheduler.events import *
from datetime import datetime, timedelta
#Use a customized version of the ShelveJobStore that uses writeback for better persistance on unexpected exits.
from jobstores.writeback_shelve_store import WriteBackShelveJobStore
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
from django.core.management import setup_environ
from ericsson_remote import settings

#Import settings from our Django App
setup_environ(settings)

#Logging
logger = logging.getLogger('dispatcher')
hdlr = logging.FileHandler('dispatcher.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.WARNING)

#Job Status Constants
JOB_NOT_SCHEDULED = 0
JOB_SCHEDULED = 1
JOB_CHANGED = 2
JOB_DELETED = 3
JOB_ERROR = 4
JOB_COMPLETED = 5

#send snmp command to change receiver settings
def change_channel(ip, polarity, frequency, symbol_rate, service_num):
    retVal = True
    
    #change polarity
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,2,2,1,0), rfc1902.Integer(polarity))
    )
    
    if errorIndication:
        retVal = False
        logger.error(errorIndication)
    
    time.sleep(.5)
    
    #frequency and symbol rate must be changed on the input we are using
    input = polarity + 1
    #change frequency
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,2,2,15,1,3,input), rfc1902.Integer(frequency))
    )
    if errorIndication:
        retVal = False
        logger.error(errorIndication)
    
    time.sleep(.5)
    
    #change symbol rate
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,2,2,15,1,4,input), rfc1902.Integer(symbol_rate))
    )  
    if errorIndication:
        retVal = False
        logger.error(errorIndication)
    
    time.sleep(.5)
    
    #change mpeg service number
    errorIndication, errorStatus, errorIndex, varBinds = cmdgen.CommandGenerator().setCmd(
    cmdgen.CommunityData('python-agent', 'private'),
    cmdgen.UdpTransportTarget((ip, 161)),
    ((1,3,6,1,4,1,1773,1,3,208,4,1,2,0), rfc1902.Integer(service_num))
    )
    
    if errorIndication:
        retVal = False
        logger.error(errorIndication)
        
    return retVal

#receiver change function
def change_it(receiver, schedule):
    return change_channel(settings.RECEIVERS[receiver], *settings.SCHEDULES[schedule])

def remove_events():
    #connect to the django database
    con = None
    con = lite.connect('ericsson_remote.sqlite')
    cur = con.cursor()
    #retrieve all jobs
    cur.execute("SELECT * from schedule_events_schedule_event")
    rows = cur.fetchall()
    for row in rows:
        if (datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S') < datetime.now() - timedelta(minutes=15)):
            cur.execute("DELETE from schedule_events_schedule_event WHERE id = ?", (row[0],))
            con.commit()
    cur.close()
    con.close()
    
#process the scheduler list - add new events, update existing, or delete
def process_events():
    #connect to the django database
    con = None
    con = lite.connect('ericsson_remote.sqlite')
    cur = con.cursor()
    #retrieve all jobs
    cur.execute("SELECT * from schedule_events_schedule_event")
    rows = cur.fetchall()
    con.close()
    for row in rows:
        status = row[4]
        if (status == JOB_NOT_SCHEDULED):
            try:
                sched.add_date_job(change_it, datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'), args=[row[2], row[3]], name=row[0], jobstore='shelve')
                set_status(row[0], JOB_SCHEDULED)
            except:
                set_status(row[0], JOB_ERROR)
        elif (status == JOB_CHANGED):
            update_job(row)
        elif (status == JOB_DELETED):
            remove_job(row[0])
    list = sched.get_jobs()
    count = 0
    for job in list:
        if job.name not in ('process_events', 'remove_events'):
            count += 1
    print str(datetime.now()) + " " + str(count) + " event(s) in the queue..."
    
#set job status
def set_status(id, status):
    print "Set status on job #" + str(id) + " to " + str(status)
    con = lite.connect('ericsson_remote.sqlite')
    cur = con.cursor()
    cur.execute("UPDATE schedule_events_schedule_event SET status = ? WHERE id = ?",  (status, id))
    con.commit()
    cur.close()
    con.close()
    
#delete event from database
def delete_event(id):
    con = lite.connect('ericsson_remote.sqlite')
    cur = con.cursor()
    cur.execute("DELETE from schedule_events_schedule_event WHERE id = ?",  (id,))
    con.commit()
    cur.close()
    con.close()
    
#remove an event from the scheduler by name
def remove_job(id):
    jobs = sched.get_jobs()
    for job in jobs:
        if (job.name == id):
            print "Deleted job #" + str(id)
            sched.unschedule_job(job)
            delete_event(id)

#update an event by name (delete and re-create)
def update_job(row):
    print "Updated job #" + str(row[0])
    jobs = sched.get_jobs()
    for job in jobs:
        if (job.name == row[0]):
            sched.unschedule_job(job)
            #add job with new details
            try:
                sched.add_date_job(change_it, datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S'), args=[row[2], row[3]], name=row[0], jobstore='shelve')
                set_status(row[0], 1)
            except:
                set_status(row[0], 4)
        #todo - if we didn't find the job for some reason go ahead and add it again?
        
#event listener          
def my_listener(event):
    if (event.job.name != 'process_events' and event.job.name != 'remove_events'):
        if (event.retval == True):
            set_status(event.job.name, 5)
            logger.info("Event #" + str(event.job.name) + " completed successfully")
        elif (event.retval == False):
            set_status(event.job.name, 4)
            logger.error("Event #" + str(event.job.name) + " had an error")
        if event.exception:
            print event.exception
            logger.fatal("Event #" + str(event.job.name) + ' - job crashed :(')
    

#start the scheduler
sched = Scheduler()
sched.add_jobstore(WriteBackShelveJobStore('jobstore.db'), 'shelve')
sched.start()

sched.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

process_events()

# Process events list every 10 seconds
sched.add_interval_job(process_events, seconds=10)

# Remove completed events from db every minute
sched.add_interval_job(remove_events, minutes=1)

print "Dispatcher started..."


try:
    while True:
        time.sleep(1)
finally:
    sched.shutdown()
