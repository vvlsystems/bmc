# Uncomment to run sample without library built or installed on system
# import sys
# sys.path.append('/local/path/to/project/vm-console-client-python')

from __future__ import print_function
import sys
sys.path.append(r'/opt/bmc/rapid7/vm-console-client-python')
import rapid7vmconsole
import base64
import logging
import sys
import time
import json
import re
from rapid7vmconsole.rest import ApiException
from pprint import pprint


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


auth = "%s:%s" % (config.username, config.password)
auth = base64.b64encode(auth.encode('ascii')).decode()
client = rapid7vmconsole.ApiClient(configuration=config)
client.default_headers['Authorization'] = "Basic %s" % auth

# create an instance of the API class
api_instance = rapid7vmconsole.ReportApi(client)
page = 0 # int | The index of the page (zero-based) to retrieve. (optional) (default to 0)
size = 1000 # int | The number of records per page to retrieve. (optional) (default to 10)
sort = ['name[,ASC]'] # list[str] | The criteria to sort the records by, in the format: `property[,ASC|DESC]`. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. (optional)
#sort = ['sort_example'] # list[str] | The criteria to sort the records by, in the format: `property[,ASC|DESC]`. The default sort order is ascending. Multiple sort criteria can be specified using multiple sort query parameters. (optional)

try:
    # Reports
    api_response = api_instance.get_reports(page=page, size=size, sort=sort)
    #pprint(api_response)

    test = api_response.resources

    for i in test:
      bmc_report = re.search("^BMC*", i.name)
      if bmc_report:
         print(i.id,"	",i.name)

    #JSON
    #json_data = json.loads(api_response.resources)

except ApiException as e:
    print("Exception when calling ReportApi->get_reports: %s\n" % e)
