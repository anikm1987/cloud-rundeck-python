# Sample python code to call rundeck job and check for status untill the job gets completed usng REST api
# Test with the jobs present inside the rundeck folder
   

import json
import requests
import sys
import time

# Defined as global variable to resolve the problem of value received as function called recursively
executionStatus=None

# Method to read config value
def getConfigValue(configGroup,configName):
    try:
     with open('config.json','r') as configFile:
      jdata = json.load(configFile)
      configValue = jdata[configGroup][configName]
      configFile.close()
      return configValue
    except FileNotFoundError :
      print ("getConfigValue ERROR : file not found  "+traceback.format_exc())
      exit(1)
    except Exception  :
      print ("getConfigValue ERROR : file read error encountered "+traceback.format_exc())
      exit(1)
 
# for creating JSON parameter request.. 
def prepareJSONrequest(status):
  return "-status {0}".format(status)

def checkForJobCompletion(jobStateURL,authToken):
    global executionStatus
    print("Checking rundeck job state using " + jobStateURL + " using authentication token")
    headers = {'Content-Type': 'application/json','X-Rundeck-Auth-Token':authToken,'Accept':'application/json'}
    response = requests.post(jobStateURL, headers=headers)
    print("Response Status Code ="+str(response.status_code))
    if response.status_code == 200:
       receivedResponse=response.json()
       print(receivedResponse)
       executionStatus=str(receivedResponse['executionState'])
       executionCompleted=str(receivedResponse['completed'])
       print("Execution status :" + executionStatus)
       print("Execution completed flag :" + executionCompleted)
       print("Execution End time :" + str(receivedResponse['endTime'])) 
       #TODO: What if the job never completes then the below loop will be infite loop
       if executionCompleted == "True":
           print(executionStatus)
       else:
           time.sleep(60)
           print("Checking for job status after 1 minute sleep")
           checkForJobCompletion(jobStateURL,authToken) 
    return executionStatus

def CallRundeckJob(jobURL,jsonParam,authToken=None):
  try:
    
    print("Calling rundeck job using " + jobURL + " using authentication token")
    headers = {'Content-Type': 'application/json','X-Rundeck-Auth-Token':authToken,'Accept':'application/json'}
    response = requests.post(jobURL, headers=headers, json = {"argString":jsonParam })
    print("Response Status Code ="+str(response.status_code))
    if response.status_code == 200:
        print('Success!')
        receivedResponse=response.json()
        print(receivedResponse)
        print("Execution Id :" + str(receivedResponse['id']))
        jobStateURL=str(receivedResponse['href']+"/state")
        print("Execution state url :" +jobStateURL )
        print("Execution Status :" + str(receivedResponse['status']))
        completedFlag=checkForJobCompletion(jobStateURL,authToken)
        print(str(completedFlag))
        
  except requests.exceptions.HTTPError as errh :
      print ("CallRundeckJob : Http Error:",errh)  
  except requests.exceptions.ConnectionError as errc:
      print ("CallRundeckJob : ConnectionError Error:",errc) 
  except requests.exceptions.Timeout as errt:
      print ("CallRundeckJob : Timeout Error:",errt)  
  except requests.exceptions.RequestException as err:
      print ("CallRundeckJob : RequestException Error:",err) 

if __name__ == "__main__":
    status= sys.argv[1]
    # To test run - python TestRundeckJobRun_Status.py Pass or python TestRundeckJobRun_Status.py Fail
    authToken= getConfigValue('rundeckInfo','authToken')
    testURL= getConfigValue('rundeckInfo','testURL')
   
    print ("testURL"+ testURL)
    
    assert testURL, 'Job URL is required'
    assert authToken, 'authToken is required'
    
    jsonParam=prepareJSONrequest(status)
    print(testURL +"======" +jsonParam)
    CallRundeckJob(testURL,jsonParam,authToken)
    