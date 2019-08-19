// Alternate JS service to access Metabase

function getmetabasequery(id,credentials){
  var service = getopenIDService(credentials.metabase);
  if (service.hasAccess()){
    idtoken = service.getToken().id_token
  }
  if (!idtoken) {throw 'OAuth error'}
  var payload = {'token':idtoken}
  var opt = {'method': 'post','contentType': 'application/json','payload': JSON.stringify(payload)}
  var mbauth = UrlFetchApp.fetch('https://uri.com/api/session/google_auth',opt)
  
  var headers={'X-Metabase-Session':JSON.parse(mbauth.getContentText()).id}
  var opt = {'method':'post','contentType': 'application/json','headers':headers,'payload':JSON.stringify({"ignore_cache":false,"parameters":[]})}
  var query='https://uri.com/api/card/'+id+'/query'
  var response = UrlFetchApp.fetch(query,opt).getContentText()
  var response = JSON.parse(response).data

  return [response.columns].concat(response.rows)
}


function getopenIDService(cred) {
  return OAuth2.createService('Google')
      // Set the endpoint URLs.
      .setAuthorizationBaseUrl('https://accounts.google.com/o/oauth2/v2/auth')
      .setTokenUrl('https://accounts.google.com/o/oauth2/token')

      // Set the client ID and secret.
      .setClientId(cred.oauth.client_id)
      .setClientSecret(cred.oauth.client_secret)

      // Set the name of the callback function that should be invoked to
      // complete the OAuth flow.
      .setCallbackFunction('authCallback')

      // Set the property store where authorized tokens should be persisted.
      .setPropertyStore(PropertiesService.getUserProperties())

      // Set the scope and additional Google-specific parameters.
      .setScope(['https://www.googleapis.com/auth/userinfo.email','https://www.googleapis.com/auth/userinfo.profile','openid'])
      .setParam('access_type', 'offline')
      .setParam('approval_prompt', 'force')
}

/**
 * Handles the OAuth callback.
 */
function authCallback(request) {
  var service = getService();
  var authorized = service.handleCallback(request);
  if (authorized) {
    return HtmlService.createHtmlOutput('Success!');
  } else {
    return HtmlService.createHtmlOutput('Denied.');
  }
}

