import requests
import hmac
from hashlib import sha1
import time
from pandas import date_range, DataFrame
import json

"""
Bank Lead Status

This file is used to extract the status of some Bank CRCD leads for a given date.
(This includes whether it is submitted, ineligible, whether the bank has called lead)

Change the date parameters to get the status of the leads known at a particular date.
Note that the application_id needs to be linked to the main DB
to get the rest of the lead details.
"""


#Date range parameters. Edit this as needed.
begin='2019-02-01'
end='2019-04-30'

apisecret='APISECRET'
apikey='APIKEY'

err=[]
data=[]

for i in date_range(begin,end):
    #Time must be in for loop as the request will be rejected if time is not within 30 seconds of request.
    tim={'time':int((time.time()-2)*1000)}
    HMAC=hmac.new(bytes(apisecret,'utf-8'),bytes(json.dumps(tim).replace(' ',''),'utf-8'),sha1)
    js={"apiKey":apikey,"data":tim,"hash":HMAC.hexdigest()}
    response=requests.post('https://url.com/{}'.format(i.strftime('%Y-%m-%d')),json=js,timeout=3000)
    if response.status_code != 200:
        err.append(response.url)
        continue
    d=response.json().get('results')
    data.extend(d)
    
if err:
    print('Error in a few responses. Please check again. \n')
    print(err)
    
df=DataFrame(data)
df.to_csv('Bank_{}_{}.csv'.format(begin,end),index=False)