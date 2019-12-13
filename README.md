# rundeck_python
##Rundeck and Python Automation

Contains -

	- rundeck
		Two yml file for creating rundeck job
			ErrorCreatorJob.yaml
			ErrorHandlerJob.yaml
		Sample job to demonstrate how to do error handling using step jobs in rundeck
		
	- python_script
	
		TestRundeckJobRun_Status.py 
			- Sample python code to call rundeck job and check for status untill the job gets completed usng REST api
			- Test with the jobs present inside the rundeck folder
