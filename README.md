# Rundeck and Python Automation

## Contains -

	- rundeck
		Two yaml file for creating rundeck job
			ErrorCreatorJob.yaml
			ErrorHandlerJob.yaml
		Sample job to demonstrate how to do error handling using step jobs in rundeck
		
	- rundeck
		yml file for creating rundeck job
			TestPythonInsideBash.yaml
		Sample job to demonstrate how to call python code from bash with arguments inside rundeck
		
	- python_script
	
		TestRundeckJobRun_Status.py 
			- Sample python code to call rundeck job and check for status untill the job gets completed usng REST api
			- Test with the jobs present inside the rundeck folder
