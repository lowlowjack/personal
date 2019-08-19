# -*- coding: utf-8 -*-
"""
Created on Tue Dec 11 11:35:04 2018

For GA related requests. Example of how to use existing library in file.

Warning: GA requests speed may vary. Try not to overload the client.
@author: Jack Low
"""


from clientsetup import garequest, init 
import pandas as pd
import os

request={
	"reportRequests":[
	{
		"viewId":'65239639',
		"dateRanges":[{"startDate":"2019-01-01", "endDate":"2019-01-10"}],
		"dimensions":[{"name":"ga:campaign"}],
		"metrics":[{"expression":"ga:sessions"},{"expression":"ga:goal7Completions"}]
		
	}]
	}
table=garequest(request)
t=table['reports'][0]['data']['rows']