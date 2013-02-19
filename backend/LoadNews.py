"""
This script spawns workers to load news from feedzilla
"""
import os
from multiprocessing import Process
import subprocess
import sys
from Queue import Queue
from threading import Thread

import mysql

def worker(queue):
    for args in iter(queue.get, None):
        try:
            subprocess.check_call(args)
        except Exception as e:
            print str(command)+" failed: "+str(e)
            

BASE_DIR = '/var/www/avenews/backend/'
PARALLELISM = 8
db = mysql.Mysql()

# Empty all the relevant tables so we can start from scratch
db.query("TRUNCATE TABLE Article;")

# Find number of countries
commands = []
for part in range(PARALLELISM):
    command = ['python', BASE_DIR+'LoadNewsWorkerCountry.py',str(part), str(PARALLELISM)]
    commands.append(command)
    
q = Queue()
threads = [Thread(target=worker, args=(q,)) for _ in range(PARALLELISM)]
for t in threads:
    t.daemon = True
    t.start()
    
for command in commands:
    print command
    q.put_nowait(command)
for _ in threads: q.put_nowait(None)
for t in threads: t.join()

"""
# Find number of states
db.query("SELECT COUNT(id) FROM State")
count = db.fetch()
count = count['COUNT(id)']

span = count/PARALLELISM
start_id = 1
for i in range(PARALLELISM):
    subprocess.Popen(['python', 'LoadNewsWorker.py','State',str(start_id),str(span)]).pid
    start_id += span

print "spawned states"

# Find number of cities
db.query("SELECT COUNT(id) FROM City")
count = db.fetch()
count = count['COUNT(id)']

span = count/PARALLELISM
start_id = 1
for i in range(PARALLELISM):
    subprocess.Popen(['python', 'LoadNewsWorker.py','City',str(start_id),str(span)]).pid
    start_id += span

print "spawned cities"

"""
