#!/usr/bin/env python
try:
    from .transfer_ujs_njs import MigrateDatabases
    from execution_engine2.db.models.models import Status, valid_status
except:
    from transfer_ujs_njs import MigrateDatabases
    from models import *


ee2_jobs = MigrateDatabases().ee2_jobs

count = 0
for job in ee2_jobs.find():
    count += 1
    job_id = job["_id"]
    status = job["status"]
    try:
        valid_status(status)
    except:
        raise Exception(job_id)
    if count % 500 == 0:
        print(f"Processed {count} records")

    if status in [Status.error.value, Status.completed.value, Status.terminated.value]:
        end_time = job.get("finished")
        if end_time is None:
            raise Exception("End time is NONE", job_id)

    if status in [Status.running.value]:
        run_time = job.get("running")
        if run_time is None:
            raise Exception("End run_time is NONE", job_id)


# Fixed finished jobs with
"""
db.getCollection('ee2_jobs').updateMany({'status' : 'finished'}, {'$set' : {'status' : 'completed'}})
db.getCollection('ee2_jobs').updateMany({'status' : 'terminated'}, {'$set' : {'finished' : 0}})

"""