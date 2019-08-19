#Json to pandas table extension. 

from flatten_json import flatten
import re 
import pandas as pd
import numpy as np

#Flatten to the ground. Note that this is a recursive operation. Requires flatten_json library, which you might need to a pip.

"""
Expects list of json as format [{},{},{}]. Make sure all the data in there has been jsonified first.
"""


def json_process(data):
    j=flatten({'data':data})
    c=re.compile('_\d+_')

    #Split the index to the common tables (newkey,previoustable,newindex,value)
    j=[(c.split(i)[-1],str(c.split(i)[:-1]),re.sub("[\[\]_' ]+",'',str(c.findall(i))),j.get(i)) for i in j.keys()]

    #Split the original into constituent dataframes by grouping by common previoustable
    j={k:list(filter(lambda x: x[1]==k,j)) for k in np.unique([i[1] for i in j])}

    #Now pivot all the columns, reformat index
    for i in j.keys():
        c=pd.Series({(k[2],k[0]):k[3] for k in j.get(i)}).unstack(level=1)
        c.index=pd.MultiIndex.from_tuples(list(map(lambda x: tuple(x.split(',')),c.index.values)))
        j.update({i:c})
    return(j)
        

