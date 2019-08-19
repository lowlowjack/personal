import os
import pandas as pd
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook import GraphAPI
#Utilizes the Facebook Business SDK.

my_app_id = 'EXAMPLEAPPID'
my_app_secret = 'xxxxxxxxxxx'


# === DEPRECATED =====
# short-lived User Token, taken from https://developers.facebook.com/tools/accesstoken/
# : Write a function to handle the expiration of the token
# : May need to look into ways to retrieve the short-term access token automatically then turn it into long-term token

### This part is needed ... when the 60 days access token expire
# Try extending the user-token by exchanging the user-token
#graph = GraphAPI(user_token)
#extended_token = graph.extend_access_token(my_app_id, my_app_secret)

#user_token_extended = extended_token['access_token']

# Write the token to a text file (not recommended)
#with open("fb_extended_token.txt", "w+") as f:
#    f.write(user_token_extended)
    
#==== DEPRECATED ====

# From now on, regenerate the token for the sysuser using the app on FB Business Manager.
# You need to be FB admin to do this.

# Read the long-term token
with open("fb_extended_token.txt") as f:
    user_token_extended = f.readline()

ad_account_id = 'ADACCOUNTID'

# Initializing the access via API
FacebookAdsApi.init(my_app_id, my_app_secret, user_token_extended)

# List all
my_account = AdAccount('act_{}'.format(ad_account_id))
#print(my_account)


fields = ['campaign_id',
          'campaign_name',
          'ad_id',
          'ad_name',
          'spend'
]
#For daily basis
'''
params = {
    'level' : 'campaign',
    'date_preset':'yesterday'
}
'''
#Batch update
params={
	'level':'campaign',
	'time_range':{'since':'2019-01-31','until':'2019-02-02'},
	'time_increment':1
}
# sample parameters format
# params = {'level': 'campaign',
#  'date_preset': 'lifetime',
#  'fields': ['account_id',
#             'account_name',
#             'actions',
#             'ad_id', 'ad_name',
#             'adset_id',
#             'adset_name',
#             'spend', ]
#  }

# retrieve a JSON look-alike object

foo = my_account.get_insights(fields=fields, params=params)

    
# flatten the object; convert to list
foo_list = [x for x in foo]
# print(type(foo_list))

# convert the list to a data frame
df = pd.DataFrame(foo_list)

df=df.rename(columns={'campaign_name':'trackingtemplate','date_start':'date'}).drop(['date_stop','id'],axis=1)

# write to csv
df.to_csv("fb.csv", index = False)
print('Facebook costs read successfully')

