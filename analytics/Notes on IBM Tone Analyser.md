#IBM Tone analyzer:


	https://developer.ibm.com/answers/questions/255295/call-to-watson-tone-analyzer-tone-analyzer-betaapi.html

Prior to using IBM Tone analyzer here are some important points to note:
I think we will have a problem in sending concurrent request to analyze sentiments as a web service. 
the error are occurring when concurrent   10-20 requests are made (which will be much more in our case if we are streaming the twitter api’s).
Plus this is a fairly new problem (Feb- 26th )

Error code looks something like:

    {
      "code" : 400,
      "error" : "The request does not contain a Content-Type"
    }
The Webservice itself  blocks concurrent requests when calling the webservice concurrently (see code 400 in the error information)

Also, we can only use curl - get to fetch the data, no python / java  api’s yet, which could be a bit cumbersome : https://www.ibm.com/smarterplanet/us/en/ibmwatson/developercloud/tone-analyzer/api/v3/?curl#post-tone
. 
####ERROR INFORMATION
- 200 - OK Success.
- 201 - OK Created.
- 400 - Bad Request Missing a required parameter or invalid parameter value.
- 401 - Unauthorized No API key provided or the API key provided was not valid.
- 404 - Not Found The requested item or parameter doesn't exist.
- 500 - Server Errors Internal server error.

> I think we shouldn’t be using ITA for analyzing streaming tweets. **Any opinions?**  
> ITA offers a huge array of other analytics options that we can call upon. 
Eg: We can get an analytics score on a bunch of tweets, that wouldn’t be realtime of course, but we perform a whole bunch of analytics on it. 

> I would say, we work on this service after our pipeline ( sharding , replication with cassandra and how to pipe that with Spark) has been made and we can call this service for some visualization after we have gathered data (may be once every day or every hour ..depends on what we do).
