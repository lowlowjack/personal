
function getfbdata(cred,params){
  // Pass in the query as the params.
  // Reference: https://developers.facebook.com/docs/marketing-api/insights/parameters#param
   
   // Builds the Facebook Ads Insights API URL
    var facebookUrl =
        'https://graph.facebook.com/v3.3' +
        '/act_' + cred.facebook.AD_ACCOUNT_ID +
        '/insights?access_token=' + cred.facebook.EXTENDED_TOKEN ;
        
    for (key in params) {
          facebookUrl += '&'+key+'='+params[key]      
        }
       
    var encodedFacebookUrl = encodeURI(facebookUrl);
    var options = {'method': 'post'};
    var fetchRequest = UrlFetchApp.fetch(encodedFacebookUrl, options);
    var results = JSON.parse(fetchRequest.getContentText());
    // Gets the csv version on facebook as JSON is not avaliable.
    var reportId = results.report_run_id;
    Logger.log('FB 1st response 200 at '+timelogging(new Date()))

    var url =
        'https://www.facebook.com/ads/ads_insights/export_report' +
        '?report_run_id=' + reportId +
        '&format=csv' +
        '&access_token=' + cred.facebook.EXTENDED_TOKEN;
  // Required so FB server has time to cache the report.
    Utilities.sleep(3000)
    var fetchRequest = UrlFetchApp.fetch(url);
    var d= Utilities.parseCsv(fetchRequest)
       Logger.log('FB extracted at '+timelogging(new Date()))
    return d
}
