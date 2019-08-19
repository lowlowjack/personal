"""
Metabase Extraction (for live connections)
"""
import requests
import pandas as pd
import getpass

##Instatiate the metabase session
auth={"username":"username", "password":getpass.getpass()}
response=requests.post('https://url/api/session',json=auth)
sessionid={'X-Metabase-Session':response.json()['id']}
del(auth)
session=requests.Session()
session.headers=sessionid


##Reading queries. Writing queries in here and passing to metabase is possible, but 
##a bit more involved than making the query in metabaase itself.

response=session.get('https://url/api/card/')
cardnames=[k['name'] for k in response.json()]

###Example query. First get associated properties of card.
def cardfind(name):
    return(response.json()[cardnames.index(name)]);
    
###Checking cardid. This can change.
ide=cardfind('Example - Funnel')['id']

##Template Tags Parameters. Optional
parameters=[{"type":"date","target":["variable",["template-tag","start_date"]],"value":"2018-10-10"},
             {"type":"date","target":["variable",["template-tag","end_date"]],"value":"2018-10-20"}]

##Query
response=session.post('https://url/api/card/'+str(ide)+'/query',json={'parameters':parameters})


##Cleaning the data
data=response.json()['data']
array={data['columns'][j]:[data['rows'][i][j] for i in range(0,len(data['rows']))] for j in range(0,len(data['columns']))}
df=pd.DataFrame(array)

