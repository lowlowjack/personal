
""" 
Creates a client for Google for various libraries with the correct authentication for offline access. 
Requires the Google APIS SDK for Python
"""

from __future__ import absolute_import

def init(name, version, doc, filename, scope=None, discovery_filename=None):
	"""Extend the file of googleapisamples on Google's SDK libraries on github
	   Author: jcgregorio@google.com (Joe Gregorio)
		"""

	from googleapiclient import discovery
	from googleapiclient.http import build_http
	import os	
	try:
		from oauth2client import client
		from oauth2client import file
		from oauth2client import tools
	except ImportError:
		raise ImportError('googleapiclient.sample_tools requires oauth2client. Please install oauth2client and try again.')

	if scope is None:
		scope = 'https://www.googleapis.com/auth/' + name

	  # Name of a file containing the OAuth 2.0 information for this
	  # application, including client_id and client_secret, which are found
	  # on the API Access tab on the Google APIs
	  # Console <http://code.google.com/apis/console>.
	client_secrets = os.path.join(os.path.dirname(filename),
							'client_secrets.json')

	  # Set up a Flow object to be used if we need to authenticate.
	flow = client.flow_from_clientsecrets(client_secrets,
										  scope=scope,
										  message=tools.message_if_missing(client_secrets))

	  # Prepare credentials, and authorize HTTP object with them.
	  # If the credentials don't exist or are invalid run through the native client
	  # flow. The Storage object will ensure that if successful the good
	  # credentials will get written back to a file.
	storage = file.Storage(name + '.dat')
	credentials = storage.get()
	if credentials is None or credentials.invalid:
		credentials = tools.run_flow(flow, storage)
	http = credentials.authorize(http=build_http())

	if discovery_filename is None:
	 # Construct a service object via the discovery service.
		service = discovery.build(name, version, http=http)
	else:
		# Construct a service object using a local discovery document file.
		with open(discovery_filename) as discovery_file:
			service = discovery.build_from_document(
					discovery_file.read(),
					base='https://www.googleapis.com/',
					http=http)
	return (service)


def screquest(request,property_uri='uri'):
    import pandas as pd

    import os
	"""
	For Search Console requests
	"""
    
    def execute_request(service, property_uri, request):
        """Executes a searchAnalytics.query request.

          Args:
            service: The webmasters service to use when executing the query.
            property_uri: The site or app URI to request data for.
            request: The request to be executed.

          Returns:
              An array of response rows.
        """
        return service.searchanalytics().query(siteUrl=property_uri, body=request).execute()
    

    
    service=init('webmasters', 'v3', __doc__, __file__,scope='https://www.googleapis.com/auth/webmasters.readonly')
    df=pd.DataFrame(execute_request(service,property_uri,request)['rows'])
    return(df.assign(keys=df['keys'].apply(lambda x:x[0])).set_index('keys'))

def garequest(request):
    """
    Similar scope to the Search Console function above, but for GA
    
    Args:
        request: The request
    
    Returns:
        json containing the request.
    """
    
    def execute_garequest(service,request):
        return service.reports().batchGet(body=request).execute()
    
    service=init('analytics','v4',__doc__,__file__,scope='https://www.googleapis.com/auth/analytics.readonly')
    return execute_garequest(service,request)

def shtrequest(spreadsheetId,ran):
    """
    Google Sheets. Same scope as above
    Args:
        spreadsheetId: string. as in 1ydI8oasNxPt_B-egg5RWIqVVrzogu5-n9FDlyF2BT5Q of 
        uri https://docs.google.com/spreadsheets/d/1ydI8oasNxPt_B-egg5RWIqVVrzogu5-n9FDlyF2BT5Q/edit?ts=5a0008ec#gid=1002417824
    
        ran: string. range of values to return in A1 notation (e.g. 'A1:B2')
        
    Returns a json object
    """
    import pandas as pd
    import os
    
    def execute_shtrequest(service,spreadsheetId,ran):
        return service.spreadsheets().values().get(spreadsheetId=spreadsheetId,range=ran).execute()
    service=init('sheets','v4',__doc__,__file__,scope='https://www.googleapis.com/auth/spreadsheets.readonly')
    return execute_shtrequest(service,spreadsheetId,ran)

    