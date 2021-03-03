# Uncomment to run sample without library built or installed on system
from __future__ import print_function
from datetime import datetime
import sys
sys.path.append(r'/opt/bmc/rapid7/vm-console-client-python')
import rapid7vmconsole
import base64
import logging
import sys
import time
import re
import requests
import json
from rapid7vmconsole.rest import ApiException
from pprint import pprint

# Credentials for Rapid 7
config = rapid7vmconsole.Configuration(name='Rapid7')
config.username = '<RAPID7-USERNAME>
config.password = '<RAPID7-PASSWORD>'
config.host = 'https://<RAPID7-FQDN>:<PORT>'
config.verify_ssl = False
config.assert_hostname = False
config.proxy = None
config.ssl_ca_cert = None
config.connection_pool_maxsize = None
config.cert_file = None
config.key_file = None
config.safe_chars_for_path_param = ''

# Logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
logger.addHandler(ch)
config.debug = False

# Encode and Setup Headers
auth = "%s:%s" % (config.username, config.password)
auth = base64.b64encode(auth.encode('ascii')).decode()
client = rapid7vmconsole.ApiClient(configuration=config)
client.default_headers['Authorization'] = "Basic %s" % auth

# Create an instance of the API class
api_instance = rapid7vmconsole.ReportApi(client)
page = 0 # int | The index of the page (zero-based) to retrieve. (optional) (default to 0)
size = 1000 # int | The number of records per page to retrieve. (optional) (default to 10)
sort = ['name[,ASC]'] # list[str] | The criteria to sort the records by, in the format: `property[,ASC|DESC]`. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. (optional)
#sort = ['sort_example'] # list[str] | The criteria to sort the records by, in the format: `property[,ASC|DESC]`. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. (optional)

try:
    # Get List of Reports
    api_response = api_instance.get_reports(page=page, size=size, sort=sort)
    reports = api_response.resources

    # Cycle through reports and select only those who's name 
    # being with "BMC"
    for i in reports:
        bmc_report = re.search("^BMC*", i.name)
        if bmc_report:
            print(i.id,"	",i.name)

            # Download the latest report results
            instance = 'latest'
            api_response_download = api_instance.download_report(i.id, instance)

	    # Timestamp to use in file scan id info as it must be
	    # unique per file
            now = datetime.now()
            date = now.strftime("%Y%m%d_%H%M%S")

            report_name_replace = i.name.replace(" ", "_")
            name = str(i.id) + "-" + report_name_replace

	    # Write the report to file
            file = open('/opt/bmc/rapid7/reports/%s.xml' % name, 'w+')
            file.write(api_response_download)
            file.close
 
            # Cycle through file contents to update the scan id for import within TSAC
            with open('/opt/bmc/rapid7/reports/%s.xml' % name, "rt") as fin:
                with open('/opt/bmc/rapid7/reports/%s.tsac.xml' % name, "wt") as fout:
                    for line in fin:
                        line_replace = re.sub(r"scan id\=\"\d+\"", 'scan id=\"%s\"' % date, line)
                        fout.write(line_replace)
                fout.close()

except ApiException as e:
    print("Exception when calling ReportApi->get_reports: %s\n" % e)
