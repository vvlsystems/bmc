# rapid7 integration to BMC Software TrueSight Automation Console
# BMC Software is a trademark, all rights reserved where appropriate
# Rapid7 Nexpose is a trademark, all rights reserved where appropriate

This integration is leveraging an unnoficial set of python modules released by Rapid 7 (https://github.com/rapid7/vm-console-client-python). 
It contains predefined activities all supported by the Rapid7 Nexpose REST API (here: https://docs.rapid7.com/nexpose/restful-api/).

It requires a few python libraries which are documented in the requirements.txt file. You must install these for it to work.

The code I created is primitive 😊 it works but could be parameterized and improved by someone with more python experience than I.  
But its important to note the requirements on the Nexpose side for this to work.

Effectively you must create an XML 2.0 report for each scan that you wish to export the results for TSAC.  There is no way in Rapid7 to associate multiple 
scans with a single XML 2.0 report.  Therefore, I suggest leveraging a naming convention that will allow the code to pull the reports you want to export 
by wildcard (e.g. use BMC in the name of report). You’ll see this in the python code.

1)	Create a user for the integration in Rapid7. User must have basic role of “User” and must have permission to access scan results and report.  
2)	Create the report(s) and associate with scan.
3)	Run the report and have it setup to auto run when scans are run, or setup a schedule basis.  

Then you can run the “download_reports.py” at your leisure:
1)	Update the config.username, config.password, and config.host  variables to reflect your Nexpose system.
2)	Update the sys.path.append to reflect the location of the vm-console-client-python directory (default is set to /opt/bmc/rapid7/vm-console-client-python)
3)	Update the wildcard search you wish to find the created reports from above (line# 60).
4)	Update the location where you want to save the location of the reports (default is set to /opt/bmc/rapid7/reports) – lines #77 and #83.
5)	Run it:

python3 download_reports.py

The report download will rename the name of the scan report inside of the file so that there is no duplication (since you can’t import duplicative scans into TSAC).  
I use a convention of date/time to do this so that the chance duplicative reports are imported is reduced.  You may find another better way to do this.

The import into TSAC is pretty uneventful, it will get the auth tokens and import a file specified as input when calling the script.
1)	Update the FQDN of TSAC in lines 8, 11, 12.
2)	Enter credentials for a user in TSAC with appropriate privileges (lines 22, 23).
3)	If you wish to use a pre-existing auth token, create a file in /opt/bmc/rapid7/tsac-rest-python/auth.token and paste the token you wish to use, and uncomment line# 49.
4)	To run it, simply run:

python3 import_scan.py <scan you wish to import>

Other utilities for unitary testing:
•	tsac-rest-python/authenticate.py – validates that you can authenticate with TSAC
•	rapid7-download-python/get_report_instance.py – allows you to download a specific report, given a specific ID.
•	rapid7-download-python/get_reports.py – allows you to list all reports available and their ID, for use in the above script. Note you have to change the filter criteria in line# 61.

If you have ideas and improvements, contribute!!
