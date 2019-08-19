//Adwords library


function getadwdata(cred,query){
  // Gets Adwords Data. 
  var adwservice = oauthservice('adwords',cred)
  // Parsing query
  var ps = pawqry(query)
  var url = 'https://googleads.googleapis.com/v1/customers/'+cred.adwords.customer_id+'/googleAds:search';
  var opt = {
                           'headers': {'Authorization': 'Bearer ' + adwservice.getAccessToken(),
                                       'Content-Type': 'application/json',
                                       'developer-token': cred.adwords.developer_token,
                                       'login-customer-id': cred.adwords.login_customer_id
                                      },
                           'method': 'post',
                           'payload': JSON.stringify(query)
                                            }
   var response = UrlFetchApp.fetch(url,opt);
  Logger.log('Adwords response 200 at '+timelogging(new Date()))
  // Parse JSON response and process to csv or spreadsheet format
  var awdata = [ps].concat(JSON.parse(response.getContentText()).results.map(function(x){return padwords(x,ps)}))
  Logger.log('Adwords extracted at '+timelogging(new Date()))
  return awdata
  
}

// Utilities to parse data
function pawqry(qry){
  var info = qry.query
  var columns = /select.+?(from)/.exec(info.toLowerCase().replace(/_./g,function subnode(match){
                    return match[1].toUpperCase()} ))[0]
  var columns = columns.slice(6,columns.indexOf("from")).replace(/ /g,'').split(',')

  return columns
}



function padwords(item,filt){
  // Function to unnest JSON data
  return filt.map(function(x){
      var res = x.split('.').reduce(function(o, k) {
        return o && o[k];
      }, item) 
      return res; 

  })  
}
