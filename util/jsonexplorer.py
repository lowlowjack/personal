# -*- coding: utf-8 -*-
"""
Created on Fri Mar  1 10:37:03 2019

Library for exploring data stored in JSON.

This doesn't preserve all data, it merely is an exploration tool to
figure out the desired columns to extract. 

@author: Jack Low
"""
import pandas as pd
import json

FILE='FILE'

##Core library that creates generator

def json_flat_to_df(json,name):
    """
    Basic recursion for flattening json
    TO-DO: Clean up the efficiency of this thing
    """
    for k in json:
        try:	
            r=json[k]
            if not isinstance(r,(list,dict)):
                yield {name+'.'+k:r}
            else:
                for i in json_flat_to_df(r,name+'.'+k):
                    yield i
        except TypeError:
            if isinstance(k,(list,dict)):
                for i in json_flat_to_df(k,name):
                    yield i
            else:
                yield {name:k}


def reader(json):
    d=dict()
    for i in json_flat_to_df(json,'$'):
        d.update(i)
    return d

###Example


with open(FILE,encoding='utf-8') as file:
    j=json.load(file)
    j=[json.loads(i['json']) for i in j]
    
j=[reader(json) for json in j]

r=pd.DataFrame(j)