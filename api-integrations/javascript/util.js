
function oauthservice(name,credentials) {
 // May need to handle invalid case to get a new refresh token. 
  // Exchanges refresh token for access token.
  // Need to elegantly stop process if user accesses OAuth flow from scratch (e.g. invalid/expired refresh token). Institute a timer. 
  
  var client = getclient(name)
  var payload = Object.create(credentials[name].oauth);
  payload.grant_type='refresh_token'
  var newToken = client.fetchToken_(payload, credentials[name].token_url);
  client.saveToken_(newToken)
  if (newToken.refresh_token) {
      client.getStorage().setValue('refresh', newToken.refresh_token)
  }
  Logger.log(name+'token extracted at '+timelogging(new Date()))
  return client
  
}

function getclient(name) {
  // Create the intial OAuth client

  return OAuth2.createService(name)
  
  // Needed to store the authorized tokens. 
      .setPropertyStore(PropertiesService.getUserProperties())

}


function readcredentials(filename) {
  // Read the credentials from file.
  var file = DriveApp.getFilesByName(filename).next() ;
  return JSON.parse(file.getBlob().getDataAsString())
  
}

function dumpsheet(sheetname,filename) {
  var sheet = SpreadsheetApp.getSheetByName(sheetname);
  var data = sheet.getDataRange().getDisplayValues();
  var data = data.map(function(item) {return item.join(',')});
  files = DriveApp.getFilesByName(filename);
  if (!files.hasNext()) {
    DriveApp.createFile(filename,data.join('\n'))
  } 
  else {
    // Be warned that this is a temporary solution. If the data exceeds 10MB, an error will be thrown.
    
    var csvdata = files.next().getBlob().getDataAsString() ;
    var csvdata = csvdata+'\n'+data.slice(1).join('\n');
    files.setContent(csvdata)
  }
}

function writejson(credentials,filename){
    var file = DriveApp.getFilesByName(filename).next() ;
   var blob = file.getBlob()
  file.setContent(JSON.stringify(credentials))
}
  
function csvtojson(val){
  var d= {}
  for (i=0;i<val[0].length;i++){
    var g = function(x,z){return x[z]}
    var f = function(z){return g(z,i)}
    d[val[0][i]]={values: val.slice(1).map(f),position:i} 
  }
  return d
}



function jsontocsv(data){
    var ls = Object.keys(data).reduce(
    function(s,x){
      s.push([x].concat(data[x].values))
      return s
    },[]
  )
  return ls.sort(function(x,y){return data[x[0]].position-data[y[0]].position})
}


function err_notification(err,mailinglist)
{
  // Sends error messages via email
  var message = 'At'+timelogging(new Date().getTime())+'/n'+err.name+err.message+'/n'+Logger.getLog()
  var options = {'noReply':true}
  GmailApp.sendEmail(mailinglist, "Error", message)
  
}

function timelogging(date){
  // For logging purposes
  return Utilities.formatDate(date, Session.getScriptTimeZone(),
      "yyyy-MM-dd'T'HH:mm:ss'Z'")
  
}

// Common aggregate functions

function sum(s,x){return s+x}
function average(s,x,i){return ((i*s)+x)/(i+1)}
function count(s,x,i,a){
  if (i==1){if(a[0]){var h=1}else{var h=0}};
  if(x){return (h||s)+1}
  else{return h||s}}