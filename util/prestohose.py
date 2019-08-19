#System for hosing leads out of Presto by a batch basis via simple FIFO queue. To be used as last resort if Presto data is processed, but unable to hose out.

from pyhive import presto
from pyhive.exc import DatabaseError 
from getpass import getpass 
from queue import Queue
import pandas as pd
import threading


hosesize=300
limit=1000
q=Queue()
lock=threading.Lock()
password=getpass()
num_worker_threads=2
timeout='50s'
output=pd.DataFrame()
logger=dict()
dbname='DBNAME'

def worker():
    while True:
        item = q.get()
        if item is None:
            break
        cursor=presto.connect(host='HOST',port=PORT,protocol='https',name='NAME',password=password,session_props={'query_max_run_time': timeout}).cursor()
        
        try:
            cursor.execute(query.format(dbname,item,item+hosesize))
            i=pd.DataFrame(cursor.fetchall(),columns=[i[0] for i in cursor.description])
           
            #Thread locking mechanism
            try:
                lock.acquire()
                output=pd.concat([output,i])
            except Exception as err:
                raise err
            finally:
                lock.release()

        except DatabaseError as err: 
            if err.args[0].get('message').find('Query exceeded maximum')>=0:
                q.put(item)
                lock.acquire()
                logger.update({})
                lock.release()
            else:
                raise
        else: 
            raise
        q.task_done()



#Customize your query.

query='''with a as (select
            data,
            row_number() over (range unbounded preceding) as rn
        from
            {} )
        select
            data
            rn
        from   
            a where rn>={} and rn<{}
        '''
cursor=presto.connect(host='HOST',port=PORT,protocol='https',name='NAME',password=password,session_props={'query_max_run_time': timeout}).cursor()

#Basic query check.
try:
    cursor.execute(query.format(dbname,0,100000))
    cursor.fetchall()
except DatabaseError as err: 
    if err.args[0].get('message').find('Query exceeded maximum')>=0:
        pass
    else:
        raise
else:
    raise


# Execute the thread flows. Make the changes in the worker function.

threads = []
for i in range(num_worker_threads):
    t = threading.Thread(target=worker)
    t.start()
    threads.append(t)

for item in range(0,limit,hosesize):
    q.put(item)

# block until all tasks are done
q.join()

# stop workers
for i in range(num_worker_threads):
    q.put(None)
for t in threads:
    t.join()

